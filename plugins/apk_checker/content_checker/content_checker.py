#!/usr/bin/env python
# coding=utf-8


# @file plugin1.py
# @brief plugin1
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2018-03-16 15:19
import os
import zipfile

import core.controllers.plugin_category as plugin_category


class ContentChecker(plugin_category.ApkChecker):
    def start(self):
        needed_file = {"AndroidManifest.xml": False,
                       "classes.dex": False,
                       "META-INF": False,
                       "res": False,
                       }
        zip_file = zipfile.ZipFile(self.apk_path)
        for name in zip_file.namelist():
            if name in needed_file.keys():
                needed_file[name] = True
            dir_name = name.split("/")[0]
            if dir_name in needed_file.keys():
                needed_file[dir_name] = True
        if False in needed_file.values():
            return False
        return True
