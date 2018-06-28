#!/usr/bin/env python
# -*- coding=utf-8 -*-

import zipfile
import subprocess

import core.controllers.plugin_category as plugin_category
import settings
from core.controllers.const import *
from core.controllers.utils import *
from core.controllers.apksec_exceptions import UnpackerException
from settings import *


class Enjarify(plugin_category.Unpacker):
    def __init__(self, task_path=None):
        plugin_category.Unpacker.__init__(self)
        url = "https://codeload.github.com/Storyyeller/enjarify/zip/master"
        name = "enjarify.zip"
        self.plugin_path = os.path.split(os.path.realpath(__file__))[0]
        download_dir = os.path.join(self.plugin_path, "bin")
        self.success, download_path = download(url, download_dir, name)
        zip_file = zipfile.ZipFile(download_path)
        zip_file.extractall(path=download_dir)
        self.bin_path = os.path.join(download_dir, "enjarify-master")

    def _ability(self):
        return {TYPE.JAR: ABILITY.B}

    def start(self):
        if not self.success:
            raise UnpackerException("enjarify not exist")
        output_path = os.path.join(self.plugin_task_path, 'backup.jar')
        if settings.OS == WINDOWS:
            python = "py -3"
        else:
            python = "python3"
        command = "{python} -O -m enjarify.main {apk_path} -f -o {output_path}".format(python=python,
                                                                                       apk_path=self.apk_path,
                                                                                       output_path=output_path)
        process = subprocess.Popen("cd {bin_path} && {command}".format(bin_path=self.bin_path,
                                                                       command=command),
                                   shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        for out_line in iter(process.stdout.readline, b''):
            logging.debug(out_line.replace('\n', '').replace('\r', ''))
        process.stdout.close()
        process.wait()
        errs = process.stderr.readlines()
        process.stderr.close()
        if len(errs):
            raise UnpackerException(''.join(errs))


if __name__ == '__main__':
    Enjarify()
