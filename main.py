import logger
import sys
import event_manager
import mister
import os
import sys
import json
import schedule
import time
import threading
import obs
import filesystem
import script
import discord
import dashboard
import retroarch
import config
import steam


if __name__ == "__main__":
    pubsub_file = "pubsub.json"

    if len(sys.argv) > 1:
        new_file = sys.argv[1]
        if os.path.exists(new_file):
            pubsub_file = new_file
            logger.info(f"Using {new_file} instead of pubsub.json")

    SETTINGS = config.get_config()

    pubsub = {}

    if os.path.exists(pubsub_file):
            with open(pubsub_file) as pubsub_json:
                pubsub = json.load(pubsub_json)

    for publisher in pubsub["publishers"]:
        if pubsub["publishers"][publisher]["status"] == "enabled":
            if publisher in event_manager.publishers:
                if "initialize" in event_manager.publishers[publisher]:
                    threading.Thread(target=event_manager.publishers[publisher]["initialize"]).start()
                refresh_rate = SETTINGS[publisher.lower()]['refresh_rate']
                schedule.every(int(refresh_rate)).seconds.do(event_manager.publishers[publisher]["publish"])

    for subscriber in event_manager.subscribers:
        if subscriber in pubsub["subscribers"]:
            if pubsub["subscribers"][subscriber]["status"] == "enabled":
                if "initialize" in event_manager.subscribers[subscriber]:
                    if "type" in pubsub["subscribers"][subscriber]:
                        if pubsub["subscribers"][subscriber]["type"] == "async":
                            event_manager.subscribers[subscriber]["initialize"]()
                    else:
                        threading.Thread(target=event_manager.subscribers[subscriber]["initialize"]).start()
                



    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            # quit
            try:
                dashboard.shutdown()
            except Exception as e:
                os._exit(0)
            sys.exit()