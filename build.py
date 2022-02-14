#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import PyInstaller.__main__
import datetime
import json

try:
    shutil.rmtree('dist')
except Exception as e:
    pass

version = "0.0"

if os.path.exists("version.json"):
    with open("version.json") as version_text:
        version_json = json.load(version_text)
        version = version_json['version']

date = datetime.datetime.now().strftime("%Y%m%d")
filename = os.path.join("release",f"GameEventHub_{version}_{date}")

#os.system('pyinstaller main.spec -i icon.ico -n test --clean -y  --add-data "templates;templates" --add-data "static;static"')
PyInstaller.__main__.run(['.\main.spec','--onefile','--clean'])
shutil.make_archive(filename, 'zip', "dist")