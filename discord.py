
from pypresence import Presence
import time
import config
import event_manager
import logger
from string_util import replace_text
from time import sleep
SETTINGS = config.get_config()

client_id = SETTINGS["discord"]['application_id']
connected = False
retries = 0
max_retries = 3

RPC = None


def update_activity(details, state, large_image=None, large_text=None, small_image=None, small_text=None, buttons=None):
    if state == "":
        state = None
    if large_image == "":
        large_image = None
    if large_text == "":
        large_text = None
    if small_image == "":
        small_image = None
    if small_text == "":
        small_text = None
    RPC.update(details=details, state=state, start=time.time(), large_image=large_image, large_text=large_text,
               small_image=small_image, small_text=small_text, buttons=buttons)  # Set the presence


def initialize():
    global RPC
    global retries
    global connected
    if retries < max_retries:
        try:
            logger.info("Attempting to connect to Discord ...")
            RPC = Presence(client_id, pipe=0)  # Initialize the client class
            RPC.connect()  # Start the handshake loop
            connected = True
            logger.info("Connected to Discord")
        except Exception as e:
            logger.error("Failed to connect to Discord: {}".format(repr(e)))
            retries += 1
            sleep(1)
            initialize()


def handle_event(event, action):
    global RPC
    if connected:
        buttons = None
        if "buttons" in action:
            buttons = action["buttons"]
        update_activity(replace_text(action["details_text"], event.tokens), replace_text(action["state_text"], event.tokens), replace_text(action["large_image"], event.tokens).lower(
        ), replace_text(action["large_text"], event.tokens), replace_text(action["small_image"], event.tokens).lower(), replace_text(action["small_text"], event.tokens), buttons)


event_manager.subscribers["Discord"] = {}
event_manager.subscribers["Discord"]["initialize"] = lambda: initialize()
event_manager.subscribers["Discord"]["handle_event"] = {
    'function': handle_event, 'arg': "args"}

if __name__ == "__main__":
    while True:
        buttons = [{"label": "Button 1", "url": "https://www.google.com"},
                   {"label": "Button 2", "url": "https://www.google.com"}]
        update_activity("Console", "Game", "segacd", None, None, None, buttons)
        time.sleep(100000)
