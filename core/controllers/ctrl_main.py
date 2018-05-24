#!/usr/bin/env python
# -*- coding=utf-8 -*-
import logging
import os
import shutil
from yapsy.PluginManager import PluginManager, PluginManagerSingleton
import settings
from core.controllers import plugin_category as catg
from core.controllers.task_info import TaskInfo
from vulnerability_database import VulnerabilityDatabase


def get_manager():
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
    return manager


def init_task(task_path):
    task_info = TaskInfo()
    task_info.task_path = task_path

    manager = get_manager()

    logging.info("Get all plugins:" + str(map(lambda e: e.name, manager.getAllPlugins())))
    return manager


def launch_apk_checker(manager):
    # 运行 apk checker
    apk_checkers = manager.getPluginsOfCategory(catg.ApkChecker.category)
    logging.info("Get apk checkers plugins:" + str(map(lambda e: e.name, apk_checkers)))
    res = []
    for each_plugin in apk_checkers:
        res.append(each_plugin.plugin_object.plugin_launch())
    if False in res:
        logging.error("Invalid apk!")
        exit(2)


def start(apk_path, ignore_plugin=[], pass_unpacker=False):
    apk_path = os.path.abspath(apk_path)

    if not os.path.exists(apk_path):
        logging.error("File not exist!")
        exit(1)

    # 建立项目目录
    task_path = create_project_dir(apk_path)
    manager = init_task(task_path)

    launch_apk_checker(manager)
    TaskInfo().pass_unpacker = pass_unpacker

    '''运行 unpacker'''
    unpackers = manager.getPluginsOfCategory(catg.Unpacker.category)
    logging.info("Get unpacker plugins:" + str(map(lambda e: e.name, unpackers)))
    from core.controllers.scheduler import unpacker_schedule
    schedule = unpacker_schedule(unpackers)
    for each_parallel in schedule:
        for each_plugin_name in each_parallel:
            each_plugin = manager.getPluginByName(each_plugin_name, catg.Unpacker.category)
            each_plugin.plugin_object.plugin_launch()

    '''运行 auditor'''
    auditors = manager.getPluginsOfCategory(catg.Auditor.category)
    logging.info("Get auditor plugins:" + str(map(lambda e: e.name, auditors)))
    for each_plugin in auditors:
        each_plugin.plugin_object.plugin_launch()

    for e in VulnerabilityDatabase().list_database():
        print e.to_dict()


def create_project_dir(apk_path):
    _dir, apk_file_name = os.path.split(apk_path)
    apk_name = apk_file_name.split('.')[0]
    task_path = os.path.join(_dir, "{}.apksec".format(apk_name))
    if not os.path.exists(task_path):
        os.mkdir(task_path)
    project_apk_path = os.path.join(task_path, settings.BACKUP_APK_NAME)
    shutil.copy(apk_path, project_apk_path)
    return task_path


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(filename)s : %(funcName)s() : %(message)s',
                        level=logging.INFO)
    # start('../../test_apks/goatdroid.apk', pass_unpacker=True)
    start('../../test_apks/goatdroid.apk')
