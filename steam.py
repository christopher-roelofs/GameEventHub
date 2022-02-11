from glob import glob
from urllib import response
from pkg_resources import DEVELOP_DIST
import requests
import json
import config
import logger
import event_manager
from mister import publish
import threading


SETTINGS = config.get_config()

last_details = {}


class SteamGameChange():
    def __init__(self, game, tokens):
        self.publisher = "Steam"
        self.event = "SteamGameChange"
        self.game = game
        self.tokens = tokens

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


api_key = SETTINGS["steam"]["api_key"]
steam_id = SETTINGS["steam"]["steam_id"]


def get_user_details():
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}"
    response = requests.get(url)
    return json.loads(response.text)["response"]["players"][0]


def get_game_details_by_id(id):
    url = f"https://store.steampowered.com/api/appdetails?appids={id}&currency=usd"
    response = requests.get(url)
    return json.loads(response.text)[id]["data"]


def initialize():
    logger.info("Initializing Steam publisher ...")


def publish():
    try:
        global last_details
        user_details = get_user_details()
        if last_details != user_details and "gameid" in user_details:
            id = user_details["gameid"]
            game_details = get_game_details_by_id(id)
            genres = []
            for item in game_details["genres"]:
                genres.append(item["description"])
            genre = ",".join(genres)
            tokens = {}
            tokens["name"] = game_details["name"]
            tokens["game_id"] = id
            tokens["description"] = game_details["short_description"]
            tokens["reference_url"] = game_details["website"]
            tokens["developer"] = ",".join(game_details["developers"])
            tokens["publisher"] = ",".join(game_details["publishers"])
            tokens["genre"] = genre
            event = SteamGameChange(game_details["name"], tokens)
            threading.Thread(target=event_manager.manage_event,
                             args=[event]).start()
            last_details = user_details
    except Exception as e:
        logger.error(f"Unable to publish SteamGameChange event")


event_manager.publishers["Steam"] = {}
event_manager.publishers["Steam"]["initialize"] = lambda: initialize()
event_manager.publishers["Steam"]["publish"] = lambda: publish()
