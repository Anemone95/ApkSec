#!/usr/bin/env python
# -*- coding=utf-8 -*-

import subprocess
import zipfile
import re
import os
import tempfile

import core.controllers.plugin_category as plugin_category
import settings
from core.controllers import const
from core.controllers.const import *
import core.controllers.controller as ctrl
from core.controllers.decorator import singleton
from core.controllers.utils import *
from core.controllers.apksec_exceptions import UnpackerException
from settings import *


class Jadx(plugin_category.Unpacker):
    def __init__(self):
        plugin_category.Unpacker.__init__(self)
        url = "https://github.com/skylot/jadx/releases/download/v0.6.1/jadx-0.6.1.zip"
        name = "jadx.zip"
        self.bin_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], "bin")
        # 下不了
        self.success, zip_path = download(url, self.bin_dir, name)
        zip_file = zipfile.ZipFile(zip_path)
        if not os.path.exists(path=self.bin_dir):
            zip_file.extractall(path=self.bin_dir)
        self.bin_path = os.path.join(self.bin_dir, "bin", "jadx")
        self.log_file = os.path.join(self.plugin_task_path, "jadx.log")

    def _ability(self):
        return {TYPE.JAVA: ABILITY.B,
                TYPE.MANIFEST: ABILITY.D,
                TYPE.XML: ABILITY.B}

    def _failed_files(self):
        with open(self.log_file, 'r') as f:
            logs = f.readlines()
        regex = re.compile(r".*ERROR\s*\-\s*Method:\s(.*)\.[a-z].*\(.*\)")
        error_classes = []
        for each_log in logs:
            res = regex.match(each_log)
            if res:
                error_classes.append(res.group(1))
        error_files = []
        for each_class in error_classes:
            error_file = self.class2abspath(each_class)
            if not os.path.exists(error_file):
                error_class = '.'.join(each_class.split('.')[:-1])
                error_file = self.class2abspath(error_class)
            error_files.append(error_file)
        return {TYPE.JAVA: error_files}

    def start(self):
        if not self.success:
            logging.error("Jadx not exist.")
            return
        # out_temp=tempfile.SpooledTemporaryFile(bufsize=100*1024)
        # fileno=out_temp.fileno()
        # process = subprocess.Popen(
        #     "{bin_path} -j 2 -d {plugin_path} {apk}".format(bin_path=self.bin_path,
        #                                                     apk=self.apk_path,
        #                                                     plugin_path=self.plugin_task_path),
        #     shell=True,
        #     stdout=fileno,
        #     stderr=subprocess.STDOUT)
        # logs = []
        # # return_code=process.poll()
        # # while return_code is None:
        # #     line=process.stdout.readline()
        # #     line=line.strip()
        # #     logging.debug(line.replace('\n', '').replace('\r', ''))
        # #     logs.append(line)
        # #     return_code=process.poll()
        # #  for out_line in iter(process.stdout.readline, b''):
        #     #  logging.debug(out_line.replace('\n', '').replace('\r', ''))
        #     #  logs.append(out_line)
        # #  process.stdout.close()
        # process.wait()
        # with open(self.log_file, 'w') as f:
        #     f.writelines(logs)

        os.system("{bin_path} -j 2 -d {plugin_path} {apk} > {log} 2>&1".format(bin_path=self.bin_path,
                                                            apk=self.apk_path,
                                                            plugin_path=self.plugin_task_path,
                                                            log=self.log_file))




if __name__ == '__main__':
    ctrl.start(r'D:\Store\document\all_my_work\CZY\ApkSec\test_apks\goatdroid.apk', skip_unpacker=True)
    jadx = Jadx()
    # print jadx.failed_files
    # print jadx.success_files(only_java=True)
