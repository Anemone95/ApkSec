#!/usr/bin/env python
# -*- coding=utf-8 -*-
import subprocess

import core.controllers.plugin_category as plugin_category
from core.controllers.const import *
from core.controllers.utils import *
from settings import *


class Apktool(plugin_category.Unpacker):
    def __init__(self):
        plugin_category.Unpacker.__init__(self)
        url = "https://github.com/iBotPeaches/Apktool/releases/download/v2.3.1/apktool_2.3.1.jar"
        name = "apktool.jar"
        self.bin_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], "bin")
        self.success, self.bin_path = download(url, self.bin_dir, name)

    def _ability(self):
        return {TYPE.SMALI: ABILITY.B,
                TYPE.ELF: ABILITY.B,
                TYPE.XML: ABILITY.B,
                TYPE.MANIFEST: ABILITY.B,
                }

    def start(self):
        if not self.success:
            logging.error("Apktool not exist.")
            return
        command = "java -jar {apktool_jar} d -f -o {output_path} {apk_path}".format(
            apktool_jar=self.bin_path,
            apk_path=self.apk_path,
            output_path=self.plugin_task_path, )
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        for out_line in iter(p.stdout.readline, b''):
            logging.debug(out_line.replace('\n', '').replace('\r', ''))
        for err_line in iter(p.stderr.readline, b''):
            logging.debug(err_line.replace('\n', '').replace('\r', ''))
        p.stdout.close()
        p.stderr.close()
        p.wait()
        if p.returncode != 0:
            raise plugin_category.UnpackerException("Apktool Failed")


if __name__ == '__main__':
    pass
