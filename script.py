import event_manager
import os
import sys
import logger


def handle_event(event,action):
    if os.path.exists(action["script"]):
        logger.event(f"Executing custom script {action['script']}: {action['description']}")
        script = open(action["script"]).read()
        #sys.argv = [action["script"], event, action ]
        exec(script)
    else:
        logger.error(f"Script not found: {action['script']}")

event_manager.subscribers["Script"] = {}
event_manager.subscribers["Script"]["handle_event"] = {'function': handle_event, 'arg': "args"}