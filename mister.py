from lib2to3.pgen2 import token
import pathlib
import config
import sys
import os
import json
import shutil
import logger
import ssh
import threading
import event_manager
import database
from time import sleep

SETTINGS = config.get_config()
RECENTS_FOLDER = '/media/{}/config/'.format(SETTINGS['mister']['core_storage'])

connected = False
ssh_session = None
retries = 0
max_retries = 3

last_game = ""
last_core = ""

map_file = "mister.json"
cores = {}


class MisterCoreChange():
    def __init__(self, system, core,tokens):
        self.publisher = "MiSTer"
        self.event = "MisterCoreChange"
        self.system = system
        self.core = core
        self.tokens = tokens
        

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class MisterGameChange():
    def __init__(self, system, core, rom,tokens):
        self.publisher = "MiSTer"
        self.event = "MisterGameChange"
        self.system = system
        self.core = core
        self.rom = rom
        self.tokens = tokens

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


def build_system_map():
    stdout = ssh_session.send_command('find /media/fat -type f -name "*.rbf"')
    stdout.sort()
    cores = {}
    for line in stdout:
        line = line.split('/')[-1].strip()
        corename = line.replace(".rbf","")
        if "_" in line:
            corename = line.split("_")[0]
    
        core = {}
        

        cores[corename] = core
    return cores

def get_cores():
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
    system_map = build_system_map()
    file_map = read_file_map()
    merged_map = system_map
    for map in file_map:
        merged_map[map] = file_map[map]
    added_maps = []
    for map in system_map:
        if map not in file_map:
            added_maps.append(map)
    if len(added_maps) > 0:
        logger.info("The following cores have been added to the mister.json: {}".format(added_maps))
        
    with open(map_file, "w") as write_file:
        json.dump(merged_map, write_file, indent=4)

def load_map_to_memory():
    global map_file
    global cores
    if os.path.exists(map_file):
        with open(map_file) as map_json:
            maps = json.load(map_json)
            cores = maps

def get_map(corename):
    if corename in cores:
        return cores[corename]
    else:
        return {}


def get_running_core():
    try:
        stdout = ssh_session.send_command("ps aux | grep [r]bf")
        current_core = 'menu'
        for line in stdout:
            if '.rbf' in line:
                for part in line.split(" "):
                    if ".rbf" in part:
                        line = part
                core_name = line.split('/')[-1].replace('.rbf','').strip()
                if "_" in core_name:
                    base_name = core_name.split('_')[0]
                    current_core = base_name

                else:
                    core_name = core_name.replace('.rbf','').strip()
                    current_core = core_name
        return current_core
    except Exception as e:
        logger.error(repr(e))
        return ""

def get_file_hash(filepath, filename):
    stdout = ""
    if ".zip" in filepath:
        stdout = ssh_session.send_command(f'unzip -p "../media/{filepath}" "{filename}" | sha1sum')
    else:
        stdout = ssh_session.send_command(f'sha1sum "../media/{filepath}/{filename}"')
    if len(stdout) > 0:
        return stdout[0].split()[0].upper()
    return ""

def get_last_game(core):
    def ignore(line):
        ignore = ["cores_recent.cfg","_shmask","_scaler","_gamma"]
        for item in ignore:
            if item in line:
                return True
        return False
    last_game = "","",""
    try:
        processes = ssh_session.send_command("ps aux | grep [r]bf")
        for line in processes:
            if ".mra" in line:
                last_game = line.split('/')[-1].replace('.mra','').strip()
                filename = line.split('/')[-1].strip()
                # adding ../ to path to match the format of the console recents file. Should probbaly not do this
                filepath = line.split(' /media/')[-1].strip().replace("/"+filename,"")
                return last_game,filepath,filename
            else:
                timeframe = 0.15 * int(SETTINGS['mister']['refresh_rate'])
                last_changed = ssh_session.send_command(f'find /media/fat/config/ -mmin -{timeframe}')
                if len(last_changed) > 0:
                    for line in last_changed:
                        if not ignore(line):
                            recent = ssh_session.send_command('strings {}'.format(line.strip()))
                            if len(recent) > 0:
                                if ".ini" not in recent[1]:
                                    return pathlib.Path(recent[1].strip()).stem,recent[0].strip()[3:],recent[1].strip()
        return last_game

    except Exception as e:
        logger.error(repr(e))
        return "","",""

def publish():
    if connected:
        global last_core
        global last_game

        core = get_running_core()
        game,filepath,filename = get_last_game(core)
        system = core
        try:
            if "system" in cores[core]:
                system = cores[core]["system"]
        except Exception as e:
            pass

        if core != "" and core != last_core:
    
            last_core = core
            if "system" in cores[core]:
                system = cores[core]["system"]
            tokens = cores[core]
            tokens["core"] = core
            event = MisterCoreChange(system,core,tokens)
            threading.Thread(target=event_manager.manage_event, args=[event]).start()

        
        if game != "" and game != last_game:
            hash = get_file_hash(filepath,filename)
            rom = {}
            if hash != "":
                rom = database.get_rom_by_hash(hash)
                if len(rom) != 0:
                    logger.info(f"Hash: {hash} matched in database")
                    system = rom["system"]
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
                event = MisterGameChange(system,core,rom,tokens)
                last_game = game
                threading.Thread(target=event_manager.manage_event, args=[event]).start()
            except Exception as e:
                logger.error(f"Unable to publish MisterGameChange event")

def initialize():
    global connected
    global ssh_session
    global retries
    if retries < max_retries:
        try:
            ipaddress = SETTINGS['mister']['ipaddress']
            username = SETTINGS['mister']['username']
            password = SETTINGS['mister']['password']
            port = SETTINGS['mister']['port']
            ssh_session = ssh.SshConnection(ipaddress,port,username,password)
            ssh_session.connect()
            logger.info("Connected to MiSTer")
            merge_maps()
            load_map_to_memory()
            connected = True
        except Exception as e:
            logger.error(f"Failed to connect to MiSTer")
            retries += 1
            initialize()


event_manager.publishers["MiSTer"] = {}
event_manager.publishers["MiSTer"]["initialize"] = lambda:initialize()
event_manager.publishers["MiSTer"]["publish"] = lambda:publish()



if __name__ == "__main__":
    initialize()
    while True:
        publish()
        sleep(1)
