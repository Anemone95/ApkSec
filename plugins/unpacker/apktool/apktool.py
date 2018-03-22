#!/usr/bin/env python
# -*- coding=utf-8 -*-
import zipfile

import core.controllers.plugin_category as plugin_category
from core.controllers.utils import *


class Apktool(plugin_category.Unpacker):
    def __init__(self, project_path=None):
        plugin_category.Unpacker.__init__(self, project_path)
        url = "https://github.com/iBotPeaches/Apktool/releases/download/v2.3.1/apktool_2.3.1.jar"
        name = "apktool.jar"
        self.bin_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], "bin")
        self.success, self.bin_path = download(url, self.bin_dir, name)

    def start(self):
        if not self.success:
            logging.error("Apktool not exist.")
            return
        stats = os.system(
            "java -jar {apktool_jar} d -f -o {output_path} {apk_path} >{normal_log} 2>{error_log}".format(
                apktool_jar=self.bin_path,
                apk_path=self.apk_path,
                output_path=self.plugin_path,
                normal_log=os.path.join(
                    self.plugin_path, "apktool.log"),
                error_log=os.path.join(
                    self.plugin_path, "error.log")
                ))


if __name__ == '__main__':
    pass
