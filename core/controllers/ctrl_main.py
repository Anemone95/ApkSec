#!/usr/bin/env python
# -*- coding=utf-8 -*-
import logging
import os
import shutil
from yapsy.PluginManager import PluginManager
import settings
from core.controllers import plugin_category as catg
import locales.i18n as i18n
_ = i18n.ugettext('apk_sec')


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

    if not os.path.exists(apk_path):
        logging.error("File not exist!")
        exit(1)

    # 建立项目目录
    project_path = create_project_dir(apk_path)
    # 初始化所有插件
    for each_plugin in manager.getAllPlugins():
        each_plugin.plugin_object.__init__(project_path)

    logging.info("Get all plugins:"+str(map(lambda e: e.name, manager.getAllPlugins())))

    # 运行 apk checker
    apk_checkers= manager.getPluginsOfCategory(catg.ApkChecker.category)
    logging.info("Get apk checkers plugins:"+str(map(lambda e: e.name, apk_checkers)))
    res = []
    for each_plugin in apk_checkers:
        res.append(each_plugin.plugin_object.start())
    if False in res:
        logging.error("Invalid apk!")
        exit(2)

    # 运行 unpacker
    unpackers = manager.getPluginsOfCategory(catg.Unpacker.category)
    logging.info("Get unpacker plugins:"+str(map(lambda e: e.name, unpackers)))
    for each_plugin in unpackers:
        logging.info("Start plugin: "+str(each_plugin.name))
        each_plugin.plugin_object.start()


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
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(filename)s : %(funcName)s() : %(message)s',
                        level=logging.INFO)
    start('../../test_apks/goatdroid.apk')
