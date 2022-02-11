import json
import os
import pathlib
from time import sleep
import time
import hashlib
import database
import zipfile
import pathlib
from os import listdir
from os.path import isfile, join
import logger
import shutil
import event_manager
import threading
import config

SETTINGS = config.get_config()

map_file = "retroarch.json"
cores = {}

retroatch_path = SETTINGS["retroarch"]["install_path"]
cores_folder = os.path.join(retroatch_path,"cores")
recents = os.path.join(retroatch_path,"content_history.lpl")
last_details = {}


class RetroarchGameChange():
    def __init__(self, system, core, rom,tokens):
        self.publisher = "Retroarch"
        self.event = "RetroarchGameChange"
        self.system = system
        self.core = core
        self.rom = rom
        self.tokens = tokens

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

def get_core_list():
    cores = {}
    onlyfiles = [pathlib.Path(f).stem.replace("_libretro","") for f in listdir(cores_folder) if isfile(join(cores_folder, f))]
    for item in onlyfiles:
        core = {}
        cores[item] = core
    return cores

def read_file_map():
    global map_file
    if os.path.exists(map_file):
        with open(map_file) as map_json:
            maps = json.load(map_json)
            return maps
    else:
        return {}

def merge_maps():
    if os.path.exists(map_file):
        logger.info("Backing up {} ...".format(map_file))
        shutil.copyfile(map_file, '{}.bak'.format(map_file))
    else:
        logger.info("No map file exists, only using map from system.")
    system_map = get_core_list()
    file_map = read_file_map()
    merged_map = system_map
    for map in file_map:
        merged_map[map] = file_map[map]
    added_maps = []
    for map in system_map:
        if map not in file_map:
            added_maps.append(map)
    if len(added_maps) > 0:
        logger.info("The following cores have been added to the retroarch.json: {}".format(added_maps))
        
    with open(map_file, "w") as write_file:
        json.dump(merged_map, write_file, indent=4)

def load_map_to_memory():
    global map_file
    global cores
    if os.path.exists(map_file):
        with open(map_file) as map_json:
            maps = json.load(map_json)
            cores = maps

def hash_zip(file):
    archive = zipfile.ZipFile(file)
    blocksize = 1024**2  #1M chunks
    for fname in archive.namelist():
        entry = archive.open(fname)
        sha1 = hashlib.sha1()
        while True:
            block = entry.read(blocksize)
            if not block:
                break
            sha1.update(block)
        return sha1.hexdigest().upper()
def hash_file(file):
    buf_size = 65536
    sha1 = hashlib.sha1()
    with open(file, 'rb') as f:
        while True:
            data = f.read(buf_size)
            if not data:
                break
            sha1.update(data)
    return format(sha1.hexdigest().upper())

def initialize():
    logger.info("Initializing Retroarch publisher ...")
    merge_maps()
    load_map_to_memory()

def publish():
    global last_details
    if os.path.exists(recents):
        access = time.time() - os.path.getmtime(recents)
        if access < int( SETTINGS["retroarch"]["refresh_rate"]):
            with open(recents) as recents_json:
                details = json.load(recents_json)
                if "items" in details:
                    if len(details["items"]) > 0:
                        if details != last_details:
                            file = details["items"][0]["path"]
                            core = pathlib.Path(details["items"][0]["core_path"]).stem.replace("_libretro","")
                            game = pathlib.Path(file).stem
                            system = core
                            try:
                                if "system" in cores[core]:
                                    system = cores[core]["system"]
                            except Exception as e:
                                pass
                            hash = ""
                            if zipfile.is_zipfile(file):
                                hash = hash_zip(file)
                            else:
                                hash = hash_file(file)
                            rom = {}
                            if hash != "":
                                rom = database.get_rom_by_hash(hash)
                                if len(rom) != 0:
                                    logger.info(f"Hash: {hash} matched in database")
                                else:
                                    logger.info(f"Hash: {hash} not matched in database")
                            if len(rom) == 0:
                                rom = database.get_rom_by_name(game,system)
                                if "rom_extensionless_file_name" in rom:
                                    logger.info(f"Rom name match in database for Game: {game}, System: {system}")
                                    system = rom["system"]
                                else:
                                    logger.info(f"Game {game} not found in database, defaulting to game")

                                    rom = vars(database.Rom())
                                    rom["release_name"] = game
                                    rom["rom_extensionless_file_name"] = game
                                    rom["system"] = system


                            try:
                                tokens = cores[core]
                                tokens["core"] = core
                                tokens.update(rom)
                                event = RetroarchGameChange(system,core,rom,tokens)
                                threading.Thread(target=event_manager.manage_event, args=[event]).start()
                            except Exception as e:
                                logger.error(f"Unabled to publish MisterGameChange event")
                            last_details = details

event_manager.publishers["Retroarch"] = {}
event_manager.publishers["Retroarch"]["initialize"] = lambda:initialize()
event_manager.publishers["Retroarch"]["publish"] = lambda:publish()

