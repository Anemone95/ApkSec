#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
from yapsy.IPlugin import IPlugin
import logging
from vulnerability_database import VulnerabilityDatabase
import settings


class ApkSecPlugin(IPlugin):
    def __init__(self, project_path=None):
        IPlugin.__init__(self)
        if project_path:
            self.project_path = project_path
            self.apk_path = os.path.join(project_path, settings.BACKUP_APK_NAME)
        self.plugin_name = self.__class__.__name__
        self.db = VulnerabilityDatabase()

    def report_vuln(self, vulnerability):
        self.db.add(vulnerability)


class ApkChecker(ApkSecPlugin):
    category = "apk_checker"

    def start(self):
        '''

        :param project_path: apk的路径
        :return True/False 一个合法/不合法的Apk
        '''
        raise NotImplementedError


class Unpacker(ApkSecPlugin):
    category = "unpacker"

    def __init__(self, project_path=None):
        ApkSecPlugin.__init__(self, project_path)
        if project_path:
            self.output_dir = os.path.join(project_path, self.plugin_name)
            if self.plugin_name != "Unpacker" and not os.path.exists(self.output_dir):
                os.mkdir(self.output_dir)

    def check_dependencies(self):
        for each_dependence in self.get_dependencies():
            if not os.path.exists(os.path.join(self.project_path, each_dependence)):
                return False
        return True

    def start(self, unpacker_path):
        '''

        :param unpacker_path: 解压到的路径 = apk文件名(projectpath)/插件名
        :return: True/False 解压成功/失败
        '''
        raise NotImplementedError


class ProtectChecker(IPlugin):
    category = "protect_checker"

    def start(self, ):
        '''

        :param project_path:
        :return: [Vulnerable]
        '''
        raise NotImplementedError


class Auditor(IPlugin):
    category = "auditor"

    def start(self, project_path):
        '''

        :param project_path:
        :return: [Vulnerable]
        '''
        raise NotImplementedError


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(filename)s : %(funcName)s : %(message)s',
                        level=logging.DEBUG)
