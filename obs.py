#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from platform import release
from urllib import request
from obswebsocket import obsws, requests  # noqa: E402
import logger
import config
import event_manager
from string_util import replace_text
import images
import threading
from time import sleep

SETTINGS = config.get_config()


ws = None
connected = False
max_retries = 3

retries = 0


def obs_call(call):
    try:
        return ws.call(call)
    except Exception as e:
        logger.error("Error making OBS call: {}.".format(repr(e)))


def disconnect():
    ws.disconnect()


def get_current_scene():
    scenes = obs_call(requests.GetSceneList())
    return scenes.getCurrentScene()


def get_scene_list():
    scenes = obs_call(requests.GetSceneList())
    return scenes.getScenes()


def is_in_scene_list(scene_name):
    scenes = obs_call(requests.GetSceneList())
    for scene in scenes.getScenes():
        if scene_name == scene['name']:
            return True
    return False


def is_in_source_list(source_name):
    sources = obs_call(requests.GetSourcesList())
    for source in sources.getSources():
        if source_name == source["name"]:
            return True
    return False


def broadcast_message(realm, message):
    requests.BroadcastCustomMessage(realm, {"message": message})
    logger.event(f'Broadcasted message "{message}" to realm {realm}')


def setSourceText(name, text):
    try:
        source_settings = obs_call(
            requests.GetSourceSettings(name)).getSourceSettings()
        logger.event('Changing source text of "{}" to "{}"'.format(name, text))
        source_settings["text"] = text
        obs_call(requests.SetSourceSettings(
            sourceName=name, sourceSettings=source_settings))
    except KeyError as e:
        logger.error(
            f'Unable to set source text for source "{name}". Source name not found')


def setSourceImage(name, file):
    try:
        source_settings = obs_call(
            requests.GetSourceSettings(name)).getSourceSettings()
        logger.event(
            'Changing source image of "{}" to "{}"'.format(name, file))
        source_settings["file"] = file
        obs_call(requests.SetSourceSettings(
            sourceName=name, sourceSettings=source_settings))
    except Exception as e:
        logger.error(
            "Unable to set source image for {}: {}".format(name, repr(e)))


def setBrowserSourceUrl(name, url):
    try:
        logger.event(
            'Changing browser source url of "{}" to "{}"'.format(name, url))
        obs_call(requests.SetBrowserSourceProperties(name, url=url))
    except Exception as e:
        logger.error(
            "Unable to set source url for {}: {}".format(name, repr(e)))


def setSourceVolume(name, volume,useDecibel=True):
    try:
        logger.event(f'Changing volume of {name} to {volume}')
        obs_call(requests.SetVolume(name, volume,useDecibel))
    except Exception as e:
        logger.error(
            f"Unable to set volume of {name} to {volume}: {e}")


def setSceneItemProperty(name, property, value):
    try:
        logger.event(
            f'Changing source property {property} of "{name}" to "{value}"')
        args = {"item": name, property: value}
        obs_call(requests.SetSceneItemProperties(**args))
    except Exception as e:
        logger.error(
            f"Unable to set source property {property} for {name}: {e}")


def change_scene(name):
    try:
        logger.event("Switching to {}".format(name))
        ws.call(requests.SetCurrentScene(name))
    except Exception as e:
        logger.error("Unable to scene to {}: {}".format(name, repr(e)))


def initialize():
    global retries
    global ws
    global connected
    if retries < max_retries:
        try:
            logger.info("Attempting to connect to OBS ...")
            ws = obsws(SETTINGS['obs']['host'], int(
                SETTINGS['obs']['port']), SETTINGS['obs']['password'])
            ws.connect()
            connected = True
            logger.info("Connected to OBS")
        except Exception as e:
            logger.error("Failed to connect to OBS: {}".format(repr(e)))
            retries += 1
            sleep(1)
            initialize()


def handle_event(event, action):
    if connected:
        if action['action'] == "ObsChangeSourceText":
            for source in action["sources"]:
                if is_in_source_list(replace_text(source, event.tokens)):
                    threading.Thread(target=setSourceText, args=[replace_text(
                        source, event.tokens), replace_text(action["sources"][source], event.tokens)]).start()
                else:
                    logger.error(
                        f"Source {replace_text(source,event.tokens)} not found")

        if action['action'] == "ObsChangeSourceImage":
            for source in action["sources"]:
                if is_in_source_list(source):
                    if action["sources"][source] == "":
                        threading.Thread(target=setSourceImage,
                                         args=[source, ""]).start()
                    else:
                        game = ""
                        release_name = ""
                        system = ""
                        if "system" in event.tokens:
                            system = event.tokens["system"]
                        if "rom" in vars(event):
                            game = event.rom["rom_extensionless_file_name"]
                            release_name = event.rom["release_name"]
                        threading.Thread(target=setSourceImage, args=[source, images.get_image(
                            action["sources"][source], system, game, release_name)]).start()
                else:
                    logger.error(f"Source {source} not found")

        if action['action'] == "ObsSetBrowserSourceUrl":
            source = replace_text(action["source"], event.tokens)
            url = replace_text(action["url"], event.tokens)
            if is_in_source_list(source):
                threading.Thread(target=setBrowserSourceUrl,
                                 args=[source, url]).start()
            else:
                logger.error(f"Source {source} not found")

        if action['action'] == "ObsSetSourceVolume":
            source = replace_text(action["source"], event.tokens)
            volume = replace_text(action["volume"], event.tokens)
            use_db = True
            if "type" in action:
                if action["type"] != "db":
                    use_db = False

            try:
                if is_in_source_list(source):
                    threading.Thread(target=setSourceVolume, args=[
                                    source, float(volume),use_db]).start()
                else:
                    logger.error(f"Source {source} not found")
            except Exception as e:
                 logger.error(f"Unable to set volume of {source} to {volume}: {e}")

        if action['action'] == "ObsSetItemProperty":
            source = replace_text(action["source"], event.tokens)
            if is_in_source_list(source):
                threading.Thread(target=setSceneItemProperty, args=[
                                 source, action["property"], action["value"]]).start()
            else:
                logger.error(f"Source {source} not found")

        if action['action'] == "ObsChangeScene":
            scene = replace_text(action["scene"], event.tokens)
            if is_in_scene_list(scene):
                threading.Thread(target=change_scene, args=[scene]).start()
            else:
                logger.error(f"Scene {scene} not found")


event_manager.subscribers["OBS"] = {}
event_manager.subscribers["OBS"]["initialize"] = lambda: initialize()
event_manager.subscribers["OBS"]["handle_event"] = {
    'function': handle_event, 'arg': "args"}

if __name__ == "__main__":
    initialize()
