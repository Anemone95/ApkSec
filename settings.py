#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os
import platform

APKSEC_DIR = os.path.split(os.path.realpath(__file__))[0]
PLUGINS_DIR = os.path.join(APKSEC_DIR, 'plugins')
BACKUP_APK_NAME = "backup.apk"
ARCH, OS = platform.architecture()
OS="ELF" if not OS else OS

if __name__ == '__main__':
    pass
