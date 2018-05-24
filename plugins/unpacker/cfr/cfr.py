#!/usr/bin/env python
# -*- coding=utf-8 -*-
import subprocess

import core.controllers.plugin_category as plugin_category
from core.controllers.apksec_exceptions import UnpackerException
from core.controllers.const import *
import core.controllers.ctrl_main as ctrl
from core.controllers.utils import *
from settings import *


class CFR(plugin_category.Unpacker):
    def __init__(self):
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
        with open(os.path.join(self.plugin_task_path, 'summary.txt'), 'r') as f:
            summary = f.read()
        failed_files = []
        for each_classes in summary.split('\n\n\n')[1:]:
            lines = each_classes.split('\n')
            for each_line in lines:
                if each_line.startswith('  '):
                    failed_files.append(self.class2abspath(lines[0]))
        return {TYPE.JAVA: failed_files}

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
            stderr=subprocess.PIPE)
        sout, serr = process.communicate()
        # 状态码为0,所有正常输出在err通道,错误输出输出在out通道
        if len(sout):
            raise UnpackerException(sout)


if __name__ == '__main__':
    ctrl.start(r'D:\Store\document\all_my_work\CZY\ApkSec\test_apks\goatdroid.apk', pass_unpacker=True)
    cfr = CFR()
    for each in cfr.success_files(only_java=True):
        print each

