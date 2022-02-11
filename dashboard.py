from glob import glob
from time import sleep
import json
from wsgiref.util import request_uri
import config
import time
from flask import Flask, request, Response, redirect, send_file, render_template
import threading
import event_manager
import logger
from PIL import Image
from io import BytesIO
import os
import base64
import images
import sys

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

SETTINGS = config.get_config()

details = {}
last_details = {}


def image_to_base64(image):
    with Image.open(image) as img:
        img = Image.open(image) 
        im_file = BytesIO()
        img.convert('RGB').save(im_file, format="PNG")
        im_bytes = im_file.getvalue()
        im_b64 = base64.b64encode(im_bytes).decode('utf-8')
        bas64String = "data:image/png;base64," + im_b64
        return bas64String

def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/')
def index():
    return render_template('details.html')

@app.route('/details')
def game_details():
    def get_game_details():
            json_data = json.dumps(details)
            yield f"data:{json_data}\n\n"
            time.sleep(int(SETTINGS["dashboard"]["refresh_rate"]))

    return Response(get_game_details(), mimetype='text/event-stream')

def initialize():
    threading.Thread(target=lambda: app.run(host=SETTINGS["dashboard"]["host"], threaded=True, port=int(SETTINGS["dashboard"]["port"]), debug=False, use_reloader=False)).start()
        



def handle_event(event,action):
    global details
    details = event.tokens.copy()
    details["boxart_image"] = ""
    details["snap_image"] = ""
    details["title_image"] = ""
    details["system_image"] = ""
    
    boxart = ""
    snap = ""
    title  = ""
    system = ""

    if "system" in details:
        system = details["system"]
        if "rom_extensionless_file_name" in details:
            boxart = images.get_boxart(system,details["rom_extensionless_file_name"],details["release_name"])
            snap = images.get_snap(system,details["rom_extensionless_file_name"],details["release_name"])
            title = images.get_title(system,details["rom_extensionless_file_name"],details["release_name"])
            system = images.get_system(system)

        if os.path.exists(boxart):
            details["boxart_image"] = image_to_base64(boxart)
        if os.path.exists(snap):
            details["snap_image"] = image_to_base64(snap)
        if os.path.exists(title):
            details["title_image"] = image_to_base64(title)
        if os.path.exists(system):
            details["system_image"] = image_to_base64(system)
        


event_manager.subscribers["Dashboard"] = {}
event_manager.subscribers["Dashboard"]["initialize"] = lambda:initialize()
event_manager.subscribers["Dashboard"]["handle_event"] = {'function': handle_event, 'arg': "args"}


