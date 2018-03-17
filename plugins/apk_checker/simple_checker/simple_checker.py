#!/usr/bin/env python
# coding=utf-8

# @file plugin1.py
# @brief plugin1
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2018-03-16 15:19
import os

import core.controllers.plugin_category as plugin_category


class SimpleChecker(plugin_category.ApkChecker):

    def start(self):
        if not os.path.exists(self.apk_path):
            return False
        if not self.apk_path.endswith('.apk'):
            return False
        return True



