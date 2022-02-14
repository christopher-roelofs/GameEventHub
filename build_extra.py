#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

try:
    shutil.rmtree('dist')
except Exception as e:
    pass
os.system('pyinstaller -i icon.ico -n DatabaseManager --clean -y -F --windowed database_manager.py')
os.system('pyinstaller -i icon.ico -n DatabaseTool --clean -y -F  database_tool.py')
shutil.copyfile('Create Patch.bat', '{0}/Create Patch.bat'.format("dist"))
shutil.copyfile('Import Patch.bat', '{0}/Import Patch.bat'.format("dist"))
shutil.copyfile('splitcores.json', '{0}/splitcores.json'.format("dist"))
shutil.copyfile('splitcores.py', '{0}/splitcores.py'.format("dist"))
shutil.copyfile('splitcores.sh', '{0}/splitcores.sh'.format("dist"))
shutil.copyfile('update_and_copy.sh', '{0}/update_and_copy.sh'.format("dist"))
shutil.make_archive(os.path.join("release","extra"), 'zip', "dist")