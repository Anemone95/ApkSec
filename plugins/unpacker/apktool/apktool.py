#!/usr/bin/env python
# -*- coding=utf-8 -*-

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
                TYPE.MANIFEST: ABILITY.C,
                }

    def start(self):
        if not self.success:
            logging.error("Apktool not exist.")
            return
        stats = os.system(
            "java -jar {apktool_jar} d -f -o {output_path} {apk_path} >{normal_log} 2>{error_log}".format(
                apktool_jar=self.bin_path,
                apk_path=self.apk_path,
                output_path=self.plugin_task_path,
                normal_log=os.path.join(
                    self.plugin_task_path, "apktool.log"),
                error_log=os.path.join(
                    self.plugin_task_path, "error.log")
                ))
        if stats != 0:
            raise plugin_category.UnpackerException("Apktool Failed")


if __name__ == '__main__':
    pass
