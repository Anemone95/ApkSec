#!/usr/bin/env python
# -*- coding=utf-8 -*-
import logging
import os

import shutil
from yapsy.PluginManager import PluginManager

import settings
from core.controllers import plugin_category as catg


def start(apk_path):
    # Load the plugins from the plugin directory.
    categories = {catg.ApkChecker.category: catg.ApkChecker,
                  catg.Unpacker.category: catg.Unpacker,
                  catg.ProtectChecker.category: catg.ProtectChecker,
                  catg.Auditor.category: catg.Auditor,
                  }

    manager = PluginManager()
    plugin_paths = map(lambda e: os.path.join(settings.PLUGINS_DIR, e), categories.keys())
    manager.setPluginPlaces(plugin_paths)
    manager.setCategoriesFilter(categories)
    manager.collectPlugins()

    # 建立项目目录
    project_path = create_project_dir(apk_path)

    for each_plugin in manager.getAllPlugins():
        each_plugin.plugin_object.__init__(project_path)

    res = []
    for each_plugin in manager.getPluginsOfCategory(catg.ApkChecker.category):
        res.append(each_plugin.plugin_object.start())
    print res

    print manager.getPluginsOfCategory(catg.Unpacker.category)

    for plugin in manager.getAllPlugins():
        print plugin.plugin_object.plugin_name


def create_project_dir(apk_path):
    _dir, apk_file_name = os.path.split(apk_path)
    apk_name = apk_file_name.split('.')[0]
    project_path = os.path.join(_dir, "{}.apksec".format(apk_name))
    if not os.path.exists(project_path):
        os.mkdir(project_path)
    project_apk_path = os.path.join(project_path, settings.BACKUP_APK_NAME)
    shutil.copy(apk_path, project_apk_path)
    return project_path


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(filename)s : %(funcName)s : %(message)s',
                        level=logging.INFO)
    start('../../test_apks/goatdroid.apk')
