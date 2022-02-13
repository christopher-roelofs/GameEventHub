from cmath import log
from platform import release
import re
import time
import config
import os
from os.path import exists
import json
from fuzzywuzzy import process
import logger

SETTINGS = config.get_config()

fuzzy_match_threshold = SETTINGS['main']['fuzzy_match_threshold']

use_fuzzy_match = SETTINGS['main']['fuzzy_match_images']
images_folder = ""
if "images_folder" in SETTINGS['main']:
    images_folder = SETTINGS['main']['images_folder']

# https://github.com/orgs/libretro-thumbnails/repositories

folder_map = {}

if os.path.exists('folder_map.json'):
    with open('folder_map.json') as map_json:
            folder_map = json.load(map_json)

def fuzzy_match(name,folder):
    files = os.listdir(folder)
    if len(files) > 0:
        highest = process.extractOne(name,files)
        if highest[1] < fuzzy_match_threshold:
            logger.info(f"Closest match {highest[0]}, match {highest[1]} under threshold of {fuzzy_match_threshold}")
            return ""
        else:
            logger.info(f"Closest match {highest[0]}, match {highest[1]} at or above threshold of {fuzzy_match_threshold}")
            return(highest[0])
    else:
        return ""

def get_boxart(system,game,release_name=""):
    if system in folder_map:
        boxart = os.path.join(images_folder, folder_map[system], folder_map['boxart_folder'], f'{game}.png')
        if not exists(boxart):
            logger.info(f"No boxart art found for {game}")
            if use_fuzzy_match and game != "":
                folder = os.path.join(images_folder, folder_map[system],folder_map['boxart_folder'])
                logger.info(f"Fuzzy match enabled, attempting to match {game} for boxart in {folder}")
                matched = ""
                try:
                    matched = fuzzy_match(game,folder)
                except Exception as e:
                    pass
                if matched == "" and release_name != "":
                    logger.info(f"Fuzzy match on {game}  failed, attempting to match {release_name} for title in {folder}")
                    try:
                        matched = fuzzy_match(release_name,folder)
                    except Exception as e:
                        pass
                if matched != "":
                    boxart = os.path.join(images_folder, folder_map[system], folder_map['boxart_folder'], matched)
                    if not exists(boxart):
                        boxart = os.path.join(images_folder, folder_map[system], folder_map['boxart_folder'], f'default.png')
                    else:
                        logger.info(f"Match {matched} found")
                else:
                    logger.info(f"No match {matched} found")
                    boxart = os.path.join(images_folder, folder_map[system], folder_map['boxart_folder'], f'default.png')
            else:
                boxart = os.path.join(images_folder, folder_map[system], folder_map['boxart_folder'], f'default.png')
        else:
            logger.info(f"Boxart art found for {game}")
        return boxart
    else:
        logger.info(f'Boxart: {system} not found in folder map. Returning ""')
        return ""
def get_snap(system,game,release_name=""):
    if system in folder_map:
        snap = os.path.join(images_folder, folder_map[system],folder_map['snap_folder'], f'{game}.png')
        if not exists(snap):
            logger.info(f"No boxart art found for {game}")
            if use_fuzzy_match and game != "":
                folder = os.path.join(images_folder, folder_map[system],folder_map['snap_folder'])
                logger.info(f"Fuzzy match enabled, attempting to match {game} for snap in {folder}")
                matched = ""
                try:
                    matched = fuzzy_match(game,folder)
                except Exception as e:
                    pass
                if matched == "" and release_name != "":
                    logger.info(f"Fuzzy match on {game}  failed, attempting to match {release_name} for title in {folder}")
                    try:
                        matched = fuzzy_match(release_name,folder)
                    except Exception as e:
                        pass
                if matched != "":
                    snap = os.path.join(images_folder, folder_map[system], folder_map['snap_folder'], matched)
                    if not exists(snap):
                        snap = os.path.join(images_folder, folder_map[system], folder_map['snap_folder'], f'default.png')
                    else:
                        logger.info(f"Match {matched} found")
                else:
                    logger.info(f"No match {matched} found")
                    snap = os.path.join(images_folder, folder_map[system], folder_map['snap_folder'], f'default.png')
            else:
                snap = os.path.join(images_folder, folder_map[system], folder_map['snap_folder'], f'default.png')
        else:
            logger.info(f"Snap art found for {game}")
        return snap
    else:
        logger.info(f'Snap: {system} not found in folder map. Returning ""')
        return ""

def get_title(system,game,release_name=""):
    if system in folder_map:
        title = os.path.join(images_folder, folder_map[system],folder_map['title_folder'], f'{game}.png')
        if not exists(title):
            logger.info(f"No title art found for {game}")
            if use_fuzzy_match and game != "":
                folder = os.path.join(images_folder, folder_map[system],folder_map['title_folder'])
                logger.info(f"Fuzzy match enabled, attempting to match {game} for title in {folder}")
                matched = ""
                try:
                    matched = fuzzy_match(game,folder)
                except Exception as e:
                    pass
                if matched == "" and release_name != "":
                    logger.info(f"Fuzzy match on {game}  failed, attempting to match {release_name} for title in {folder}")
                    try:
                        matched = fuzzy_match(release_name,folder)
                    except Exception as e:
                        pass
                if matched != "":
                    title = os.path.join(images_folder, folder_map[system], folder_map['title_folder'], matched)
                    if not exists(title):
                        title = os.path.join(images_folder, folder_map[system],folder_map['title_folder'], f'default.png')
                    else:
                        logger.info(f"Match {matched} found")
                else:
                    logger.info(f"No match {matched} found")
                    title = os.path.join(images_folder, folder_map[system],folder_map['title_folder'], f'default.png')
            else:
                title = os.path.join(images_folder, folder_map[system], folder_map['title_folder'], f'default.png')
        else:
            logger.info(f"Title art found for {game}")
        return title
    else:
        logger.info(f'Title: {system} not found in folder map. Returning ""')
        return ""

def get_system(system):
    if system in folder_map:
        system_image = os.path.join(images_folder,folder_map['system_folder'], f'{system.replace("/","-")}.png')
        if not exists(system_image):
            system_image = os.path.join(images_folder, folder_map['system_folder'], f'default.png')
        logger.info(f"System art found for {system}")
        return system_image
    else:
        logger.info(f'System: {system} not found in folder map. Returning ""')
        return ""

def get_image(image_type,system,game,release_name=""):
    if image_type == "boxart":
        return get_boxart(system,game,release_name)
    if image_type == "snap":
        return get_snap(system,game,release_name)
    if image_type == "title":
        return get_title(system,game,release_name)
    if image_type == "system":
        return get_system(system)
    return image_type

if __name__ == "__main__":
    #print(get_game_images("Nintendo Game Boy Advance", "Punisher, The (USA)")[0])
    #fuzzy_match("Arkanoid (Unl. Lives, slower) [hb]")
    fuzzy_match("Street Fighter Alpha 2 (EU, 960229)")