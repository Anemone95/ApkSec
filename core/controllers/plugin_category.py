#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
from yapsy.IPlugin import IPlugin
import logging

from core.controllers.apksec_exceptions import *
from core.controllers.const import TYPE
from core.controllers.file_provider import FileProvider
from core.controllers.task_info import TaskInfo
from vulnerability import Vulnerability, VulnReport
from report_database import ReportDatabase


class ApkSecPlugin(IPlugin):
    """
    xxx_path: 是指扫描项目的目录/文件，dir指ApkSec项目中的目录
    """

    def __init__(self):
        IPlugin.__init__(self)
        self.file_provider = FileProvider()
        self.plugin_name = self.__class__.__name__
        self.db = ReportDatabase()
        self.task_info = TaskInfo()
        self.register_vulns()

    @property
    def task_path(self):
        return TaskInfo().task_path

    @property
    def apk_path(self):
        return TaskInfo().apk_path

    def register_vuln(self, vuln=None, name=None, i18n_name=None, category=None, description=None, solution=None,
                      risk_level=None):
        if not vuln:
            vuln = Vulnerability(name=name, i18n_name=i18n_name, category=category, description=description,
                                 solution=solution,
                                 risk_level=risk_level)
        report = self.db.filter(name=vuln.name, plugin_name=self.plugin_name)
        if len(report):
            return
        report = VulnReport(vuln, plugin_name=self.plugin_name)
        self.db.add(report)

    def register_vulns(self):
        pass

    def report_vuln(self, vuln, reference):
        if type(vuln) == str:
            vuln_name = vuln
        else:
            vuln_name = vuln.name
        report = self.db.filter(name=vuln_name, plugin_name=self.plugin_name)
        if len(report) == 0:
            err_str = "Database doesn't have this vulnerability"
            raise PluginException(err_str)
        elif len(report) > 1:
            err_str = "Duplicate vulnerabilities. Check your plugin register"
            raise PluginException(err_str)
        report = report[0]
        report.reference.append(reference)
        logging.warning(
            "Plugin {plugin_name} find vulnerability: {vuln_name} in {location}".format(plugin_name=self.plugin_name,
                                                                                        vuln_name=vuln_name,
                                                                                        location=reference.location))

    def start(self):
        """
        所有插件实现该方法
        """
        raise NotImplementedError

    def plugin_launch(self):
        """
        控制器调用该方法，该方法调用各个插件的start方法
        :return:
        """
        logging.info("Start plugin: " + str(self.plugin_name))
        res = self.start()
        _task_info = TaskInfo()
        _task_info.finished_plugin.append(self.plugin_name)
        return res


class ApkChecker(ApkSecPlugin):
    category = "apk_checker"

    def start(self):
        """

        :return True/False 一个合法/不合法的Apk
        """
        raise NotImplementedError

    def plugin_launch(self):
        valid = ApkSecPlugin.plugin_launch(self)
        if not valid:
            logging.error("Plugin: {} detects input is an invalid apk".format(self.plugin_name))
        return valid


class Unpacker(ApkSecPlugin):
    category = "unpacker"

    def __init__(self):
        ApkSecPlugin.__init__(self)
        self.plugin_task_path = os.path.join(self.task_path, "unpacker", self.plugin_name)
        if self.plugin_name != "Unpacker" and not os.path.exists(self.plugin_task_path):
            os.makedirs(self.plugin_task_path)
        self.failed_files_cache = None

    def _failed_files(self):
        """
        插件复写该方法，返回解析失败的文件类型和列表
        :return: {FILE_TYPE.JAVA:[aaa.java,bbb.java,...]} 返回绝对路径
        """
        return {}

    # @property
    # def failed_files(self):
    #     """
    #     外部调用该方法，进行统计，返回一个文件失败多少次, 比如java文件中2个方法未解析成功
    #     使用 plugin.failed_files[FILE_TYPE].keys() 可以获得某类文件集合
    #     :return: {FILE_TYPE: {"aaa.java":1} }
    #     """
    #     if not self.failed_files_cache:
    #         self.failed_files_cache = {}
    #         files = self._failed_files()
    #         for each_file_type in files:
    #             self.failed_files_cache[each_file_type] = Unpacker.__summary(files[each_file_type])
    #     return self.failed_files_cache

    @property
    def failed_files(self):
        """
        外部调用该方法，进行统计，返回一个文件失败多少次, 比如java文件中2个方法未解析成功
        使用 plugin.failed_files[FILE_TYPE].keys() 可以获得某类文件集合
        :return: {FILE_TYPE: {"aaa.java":1} }
        """
        # TODO 由于类不是单例，所以没用
        if not self.failed_files_cache:
            self.failed_files_cache = {}
            files = self._failed_files()
            for each_file_type in files:
                self.failed_files_cache[each_file_type] = Unpacker.__summary(files[each_file_type])
        return self.failed_files_cache

    @staticmethod
    def __summary(files):
        dic = dict((each, 0) for each in files)
        for each in files:
            dic[each] += 1
        return dic

    '''每一插件允许依赖某些插件产生的结果，但是只能依赖文件类型而不是依赖某个插件'''

    def _dependencies(self):
        return ()

    @property
    def dependencies(self):
        if isinstance(self._dependencies(), type(TYPE.JAVA)):
            return (self._dependencies(),)
        return self._dependencies()

    def _ability(self):
        return NotImplementedError

    @property
    def ability(self):
        """
        设置该插件的解析文件类型，和解析文件能力，如:
        {   FILE_TYPE.XML: ABILITY.A,
            FILE_TYPE.JAVA: ABILITY.B,
        }
        """
        return self._ability()

    def success_files(self, only_java=False):
        """

        :param only_java: 打开该选项则只返回本包的java文件
        :return: 返回绝对路径
        """
        failed_files = []
        # 这里获取了所有错误的文件，self.failed_files.values()原格式为字典，隐式转换为列表
        map(failed_files.extend, self.failed_files.values())

        list_dirs = os.walk(self.plugin_task_path)
        ret = []
        for root, dirs, files in list_dirs:
            for f in files:
                file_path = os.path.join(root, f)
                if only_java:
                    if self.task_info.package_name.replace('.', os.path.sep) not in file_path:
                        continue
                ret.append(file_path)

        failed = set(failed_files)
        succ = set(ret) - failed
        return succ

    def start(self):
        """
        :return: True/False 解压成功/失败
        """
        raise NotImplementedError

    def plugin_launch(self):
        """
        只有成功解压的才注册unpacker
        :return:
        """
        res = ApkSecPlugin.plugin_launch(self)
        self.file_provider.register_unpacker(self)
        return res

    def path2class(self, file_path, plugin_task_path=None):
        if not plugin_task_path:
            plugin_task_path = self.plugin_task_path
        java_class = os.path.relpath(os.path.splitext(file_path)[0], plugin_task_path) \
            .replace(os.path.sep, '.')
        return java_class

    def class2relpath(self, java_class):
        path = os.path.join('{}.java'.format(java_class.replace('.', os.path.sep)))
        return path

    def class2abspath(self, java_class, plugin_task_path=None):
        if not plugin_task_path:
            plugin_task_path = self.plugin_task_path
        path = os.path.join(plugin_task_path, self.class2relpath(java_class))
        return path

    def abspath2relpath(self, abs_path):
        return os.path.sep.join(os.path.relpath(abs_path, self.task_path).split(os.path.sep)[2:])


class ProtectChecker(ApkSecPlugin):
    category = "protect_checker"

    def start(self):
        """
        :return: [Vulnerable]
        """

        raise NotImplementedError


class Auditor(ApkSecPlugin):
    category = "auditor"

    def __init__(self):
        ApkSecPlugin.__init__(self)
        self.plugin_task_path = os.path.join(self.task_path, "auditor", self.plugin_name)
        if self.plugin_name != "Auditor" and not os.path.exists(self.plugin_task_path):
            os.makedirs(self.plugin_task_path)

    def register_vulns(self):
        logging.warning("{} doesn't register any vulnerability.".format(self.plugin_name))

    def start(self):
        """

        :return: [Vulnerable]
        """
        raise NotImplementedError


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(filename)s : %(funcName)s : %(message)s',
                        level=logging.DEBUG)
