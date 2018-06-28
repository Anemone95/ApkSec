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


class Procyon(plugin_category.Unpacker):
    def __init__(self, task_path=None):
        plugin_category.Unpacker.__init__(self)
        url = "https://bitbucket.org/mstrobel/procyon/downloads/procyon-decompiler-0.5.30.jar"
        name = "procyon.jar"
        self.bin_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], "bin")
        self.success, self.bin_path = download(url, self.bin_dir, name)

    def _dependencies(self):
        return TYPE.JAR

    def _ability(self):
        return {TYPE.JAVA: ABILITY.B}

    def _failed_files(self):
        failed_pattern = "This method could not be decompiled."
        failed_files = []
        for root, dirs, files in os.walk(self.plugin_task_path):
            for each_file in files:
                file_path = os.path.join(root, each_file)
                with open(file_path, 'r') as f:
                    failed_times = f.read().count(failed_pattern)
                    for i in xrange(failed_times):
                        failed_files.append(file_path)
        return {TYPE.JAVA: failed_files}

    def start(self):
        if not self.success:
            raise UnpackerException("procyon not exist")
        jar_paths = self.file_provider.get_files_by_type(TYPE.JAR)
        if not jar_paths:
            raise UnpackerException("No backup.jar")
        jar_path = jar_paths[0]
        process = subprocess.Popen(
            "java -Xmx10g -Xms4g -jar {procyon} {jar} -o {output_dir}".format(procyon=self.bin_path,
                                                               jar=jar_path,
                                                               output_dir=self.plugin_task_path),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        logs = []
        for out_line in iter(process.stdout.readline, b''):
            logging.debug(out_line.replace('\n', '').replace('\r', ''))
            logs.append(out_line)
        process.stdout.close()
        process.wait()

        errs = process.stderr.readlines()
        process.stderr.close()

        if process.returncode != 0:
            raise UnpackerException("Procyon error: "+''.join(errs))
        if len(errs):
            raise UnpackerException("Procyon error: "+''.join(errs))


if __name__ == '__main__':
    TaskInfo().task_path = r'D:\Store\document\all_my_work\CZY\ApkSec\test_apks\goatdroid.apksec'
    proc = Procyon()
    print proc.failed_files
