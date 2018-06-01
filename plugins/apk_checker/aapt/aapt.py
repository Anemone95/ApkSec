#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import subprocess
import logging
import re

import core.controllers.plugin_category as plugin_category
import core.controllers.task_info as task_info
import core.controllers.apksec_exceptions as apksec_exceptions
import settings


class AAPT(plugin_category.ApkChecker):
    def start(self):
        _task_info = task_info.TaskInfo()
        if settings.OS == 'WindowsPE':
            bin_path = os.path.join('windows_64bit', 'aapt.exe')
        elif settings.OS == 'ELF':
            if settings.ARCH == '64bit':
                bin_path = os.path.join('linux_64bit', 'aapt')
            else:
                bin_path = os.path.join('linux_32bit', 'aapt')
        else:
            raise apksec_exceptions.PluginException('Unknown System')
        bin_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'bin', bin_path)
        process = subprocess.Popen('{aapt} dump badging {apk_path}'.format(aapt=bin_path, apk_path=self.apk_path),
                                   shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        aapt_res, err = process.communicate()
        if len(err):
            logging.error('aapt error: {}'.format(err))
            return False
        aapt_res = aapt_res.replace('\n', '').replace('\r', '')

        regex_package_name = r"package: name='([a-z\.]*)'"
        match_res = re.match(regex_package_name, aapt_res)
        if match_res:
            _task_info.package_name = match_res.group(1)
        else:
            raise apksec_exceptions.ApkCheckerException("Unknown package name.")

        regex_main_activity = r".*launchable\-activity: name='([a-zA-Z\.]*)'"
        match_res = re.match(regex_main_activity, aapt_res)
        if match_res:
            _task_info.main_activity = match_res.group(1)
        else:
            raise apksec_exceptions.ApkCheckerException("Unknown main activity.")

        regex_target_sdk = r".*targetSdkVersion:'([1-9]\d*)'"
        match_res = re.match(regex_target_sdk, aapt_res)
        if match_res:
            _task_info.target_sdk = int(match_res.group(1))
        else:
            raise apksec_exceptions.ApkCheckerException("Unknown target sdk.")
        return True

if __name__ == '__main__':
    pass
