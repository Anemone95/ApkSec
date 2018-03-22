#!/usr/bin/env python
# -*- coding=utf-8 -*-

import core.controllers.plugin_category as plugin_category
import os
import logging
import zipfile

from core.controllers.utils import *


class Jadx(plugin_category.Unpacker):
    def __init__(self, project_path=None):
        plugin_category.Unpacker.__init__(self, project_path)
        url = "https://github.com/skylot/jadx/releases/download/v0.6.1/jadx-0.6.1.zip"
        name = "jadx.zip"
        self.bin_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], "bin")
        # 下不了
        self.success, zip_path = download(url, self.bin_dir, name)
        zip_file = zipfile.ZipFile(zip_path)
        zip_file.extractall(path=self.bin_dir)
        self.bin_path = os.path.join(self.bin_dir, "bin", "jadx")

    def start(self):
        if not self.success:
            logging.error("Jadx not exist.")
            return
        stats = os.system(
            "{bin_path} -d {plugin_path} {apk} -e >{normal_log} 2>{error_log}".format(bin_path=self.bin_path,
                                                                                      apk=self.apk_path,
                                                                                      plugin_path=self.plugin_path,
                                                                                      normal_log=os.path.join(
                                                                                          self.plugin_path, "jadx.log"),
                                                                                      error_log=os.path.join(
                                                                                          self.plugin_path, "error.log")
                                                                                      ))


if __name__ == '__main__':
    a = Jadx("test_apks/goatdroid.apksec")
    # print a.start()
    # print get_from_to(r"D:\Store\document\all_my_work\CZY\ApkSec\test_apks\goatdroid.apksec", from_plugin="Unzip",
    #                   to_plugin="AXMLPrinter", magic="\x03\x00\x08\x00")
