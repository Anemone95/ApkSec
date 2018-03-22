#!/usr/bin/env python
# coding=utf-8

# @file plugin1.py
# @brief plugin1
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2018-03-16 15:19
import os
import logging
import core.controllers.plugin_category as plugin_category
import locales.i18n as i18n

_ = i18n.ugettext('apk_sec')


class FileChecker(plugin_category.ApkChecker):
    def start(self):
        if not self.apk_path.endswith('.apk'):
            return False
        status = os.system("file --version > {}".format(os.path.join(self.project_path, 'file_version')))
        if status != 0:
            logging.warning(_("The system does not have 'file' command, so file checker doesn't work."))
            return True
        result = os.popen("file {}".format(self.apk_path))
        if "JAR" not in result.readlines()[0]:
            return False
        return True
