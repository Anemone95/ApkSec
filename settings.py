#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os
import platform

APKSEC_DIR = os.path.split(os.path.realpath(__file__))[0]
PLUGINS_DIR = os.path.join(APKSEC_DIR, 'plugins')
BACKUP_APK_NAME = "backup.apk"
ARCH, OS = platform.architecture()

if __name__ == '__main__':
    pass
