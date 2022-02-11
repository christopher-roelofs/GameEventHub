import event_manager
import os
import json





def handle_event(event,action):
    pass






event_manager.subscribers["Filesystem"] = {}
event_manager.subscribers["Filesystem"]["handle_event"] = {'function': handle_event, 'arg': "args"}