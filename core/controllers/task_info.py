#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os

import settings
from core.controllers.apksec_exceptions import TaskInfoException
from core.controllers.decorator import singleton


@singleton
class TaskInfo(object):
    def __init__(self):
        self.package_name = None
        self.main_activity = None
        self.target_sdk = None
        self.finished_plugin = []
        self.__task_path = None
        self.apksec_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', '..')

    @property
    def task_path(self):
        return self.__task_path

    @task_path.setter
    def task_path(self, path):
        self.__task_path = os.path.abspath(path)

    @property
    def apk_path(self):
        if self.task_path:
            return os.path.join(self.task_path, settings.BACKUP_APK_NAME)
        else:
            raise TaskInfoException("Task path not set.")


if __name__ == '__main__':
    task_info = TaskInfo()
    task_info.task_path = 'aa'
    task_info2 = TaskInfo()
    print task_info2.apk_path
