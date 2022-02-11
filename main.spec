# -*- mode: python ; coding: utf-8 -*-

import glob

block_cipher = None


a = Analysis(['main.py'],
             pathex=['.'],
             binaries=[],
             datas=[('templates', 'templates'), ('static', 'static')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='GameEventHub',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          icon='./icon.ico',
          console=True )

import shutil
shutil.copyfile('mister.json', '{0}/mister.json'.format(DISTPATH))
shutil.copyfile('config.json.template', '{0}/config.json'.format(DISTPATH))
shutil.copyfile('database.json', '{0}/database.json'.format(DISTPATH))
shutil.copyfile('folder_map.json', '{0}/folder_map.json'.format(DISTPATH))
shutil.copyfile('pubsub.json', '{0}/pubsub.json'.format(DISTPATH))
shutil.copyfile('retroarch.json', '{0}/retroarch.json'.format(DISTPATH))