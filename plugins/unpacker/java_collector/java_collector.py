#!/usr/bin/env python
# -*- coding=utf-8 -*-
import shutil
import copy

import core.controllers.plugin_category as plugin_category
import core.controllers.ctrl_main as ctrl
from core.controllers.const import *
from core.controllers.task_info import TaskInfo
from core.controllers.utils import *
from settings import *


class JavaCollector(plugin_category.Unpacker):
    def __init__(self, task_path=None):
        plugin_category.Unpacker.__init__(self)
        """do something"""

    def _dependencies(self):
        return TYPE.JAVA

    def _ability(self):
        return {TYPE.JAVA: ABILITY.A}

    def start(self):
        manager = ctrl.get_manager()
        package_name = self.task_info.package_name
        decompilers = manager.getPluginsOfCategory(plugin_category.Unpacker.category)
        decompilers = map(lambda e: e.plugin_object, decompilers)
        decompilers = filter(lambda e: TYPE.JAVA in e.failed_files, decompilers)

        """获取每个反编译插件的文件白名单"""
        logging.info("Find decompilers: {}".format(decompilers))

        successful_files = {}
        for each_decompiler in decompilers:
            files_list = self.file_provider.get_files(each_decompiler.plugin_name, '.*.java')
            successful_files[each_decompiler.plugin_name] = map(lambda e: self.abspath2relpath(e), files_list)
        failed_files = {}
        for each_decompiler in decompilers:
            failed_files[each_decompiler.plugin_name] = {}
            for each_path, num in each_decompiler.failed_files[TYPE.JAVA].iteritems():
                failed_files[each_decompiler.plugin_name][self.abspath2relpath(each_path)] = num
        """合并所有文件"""
        successful_files_list = []
        map(successful_files_list.extend, successful_files.values())  # 合并白名单文件
        files_set = copy.copy(successful_files_list)
        # 合并黑名单文件，因为failed_files为{decompiler: {file:failed_times}} 所以要做第二次map
        failed_files_list = map(lambda e: e.keys(), failed_files.values())
        map(files_set.extend, failed_files_list)
        files_set = set(files_set)
        suffix = package_name.replace('.', os.path.sep)
        files_set = filter(lambda f: f.startswith(suffix), files_set)

        """获取每一文件，依次遍历每个插件的白名单，若遗漏了某文件则在黑名单中选错误最少的一个"""
        log_improve = ""
        for each_decompiler in successful_files:
            log_improve += "{}: {}, ".format(each_decompiler, len(successful_files[each_decompiler]))
        log_improve += "Total: {}".format(len(set(successful_files_list)))
        logging.info(log_improve)
        for each_file in files_set:
            unpacker_name = JavaCollector.get_file_from_succ_file(each_file, successful_files)
            if not unpacker_name:
                unpacker_name = JavaCollector.get_file_from_failed_file(each_file, failed_files)
            src_path = os.path.join(self.task_path, 'unpacker', unpacker_name, each_file)
            dest_path = os.path.join(self.plugin_task_path, each_file)
            try:
                shutil.copy(src_path, dest_path)
            except IOError:
                os.makedirs(os.path.dirname(dest_path))
                shutil.copy(src_path, dest_path)

    @staticmethod
    def get_file_from_succ_file(filename, successful_files):
        res = filter(lambda e: filename in e[1], successful_files.iteritems())
        if len(res):
            return res[0][0]
        else:
            return None

    @staticmethod
    def get_file_from_failed_file(filename, failed_files):
        succ_decompiler = None
        min_times = 999999
        for each_decompiler in failed_files.keys():
            if filename in failed_files[each_decompiler].keys():
                if failed_files[each_decompiler][filename] < min_times:
                    succ_decompiler = each_decompiler
                    min_times = failed_files[each_decompiler][filename]
                pass
        return succ_decompiler


if __name__ == '__main__':
    ctrl.start(r'D:\Store\document\all_my_work\CZY\ApkSec\test_apks\goatdroid.apk', pass_unpacker=True)
    javacollector = JavaCollector()
    javacollector.start()
