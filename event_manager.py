import os
import json
import logger

publishers = {}
subscribers = {}

pubsub = {}

if os.path.exists("pubsub.json"):
        with open("pubsub.json") as subsub_json:
            pubsub = json.load(subsub_json)

def manage_event(event):
    logger.event(f"Managing {event.event} from {event.publisher}")
    for subscriber in subscribers:
        if subscriber in pubsub["subscribers"]:
            if pubsub["subscribers"][subscriber]["status"] == "enabled":
                subscriptions = pubsub["subscribers"][subscriber]["subscribed_events"]
                for subscription in subscriptions:
                    for key in subscription.keys():
                        if key == event.event:
                            for action in subscription[key]:
                                if action["status"] == "enabled":
                                    subscribers[subscriber]["handle_event"]["function"](event,action)


if __name__ == "__main__":
    pass
