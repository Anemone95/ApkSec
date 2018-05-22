#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os

import settings
from core.controllers.apksec_exceptions import TaskInfoException


class TaskInfo(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(TaskInfo, cls).__new__(cls, *args, **kwargs)
            cls._instance.package_name = None
            cls._instance.main_activity = None
            cls._instance.target_sdk = None
            cls._instance.finished_plugin = []
            cls._instance.__task_path = None
        return cls._instance

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
