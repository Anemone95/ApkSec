#!/usr/bin/env python
# -*- coding=utf-8 -*-
import zipfile

import subprocess

import core.controllers.plugin_category as plugin_category
from core.controllers.apksec_exceptions import UnpackerException
from core.controllers.const import *
from core.controllers.task_info import TaskInfo
from core.controllers.utils import *
from settings import *


class CFR(plugin_category.Unpacker):
    def __init__(self, task_path=None):
        plugin_category.Unpacker.__init__(self)
        url = "http://www.benf.org/other/cfr/cfr_0_129.jar"
        name = "cfr.jar"
        self.bin_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], "bin")
        self.success, zip_path = download(url, self.bin_dir, name)
        self.bin_path = os.path.join(self.bin_dir, "cfr.jar")

    def _dependencies(self):
        return TYPE.JAR

    def _ability(self):
        return {TYPE.JAVA: ABILITY.B}

    def _failed_files(self):
        with open(os.path.join(self.plugin_task_path,'summary.txt'), 'r') as f:
            summary=f.readlines()
        failed_classes=[]
        for row in xrange(len(summary)):
            if summary[row].startswith('---------'):
                failed_classes.append(summary[row-1].strip('\n').strip('\r'))
        return {TYPE.JAVA_CLASS: failed_classes}

    def start(self):
        if not self.success:
            raise UnpackerException("cfr not exist")
        jar_paths = self.file_provider.get_files_by_type(TYPE.JAR)
        if not jar_paths:
            raise UnpackerException("No backup.jar")
        jar_path = jar_paths[0]
        process = subprocess.Popen(
            "java -jar {cfr} {jar} --outputdir {output_dir}".format(cfr=self.bin_path,
                                                                    jar=jar_path,
                                                                    output_dir=self.plugin_task_path),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        sout, serr = process.communicate()


if __name__ == '__main__':
    TaskInfo().task_path = r'D:\Store\document\all_my_work\CZY\ApkSec\test_apks\goatdroid.apksec'
    cfr = CFR()
    print cfr.failed_files
