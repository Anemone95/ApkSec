#!/usr/bin/env python
# -*- coding=utf-8 -*-

import core.controllers.plugin_category as plugin_category
import logging
from core.controllers.utils import *


class AXMLPrinter(plugin_category.Unpacker):
    def __init__(self, project_path=None):
        plugin_category.Unpacker.__init__(self, project_path)
        self.dependencies = ["Unzip"]
        self.bin_url = "https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/android4me" \
                       "/AXMLPrinter2.jar"
        self.bin_name = "AXMLPrinter2.jar"
        self.bin_dir = os.path.join(os.path.split(os.path.realpath(__file__))[0], "bin")
        self.has_axmlprinter, self.bin_path = download(self.bin_url, self.bin_dir, self.bin_name)

    def start(self):
        if not self.has_axmlprinter:
            logging.error("AXMLPrinter2.jar not exist.")
            return
        for from_xml, to_xml in get_from_to(self.project_path, "Unzip", "AXMLPrinter", magic="\x03\x00\x08\x00"):
            tmp_dir = os.path.split(to_xml)[0]
            if not os.path.exists(tmp_dir):
                os.makedirs(tmp_dir)
            stats = os.system("java -jar {jar_path} {axml} > {xml} 2>1".format(jar_path=self.bin_path,
                                                                               axml=from_xml,
                                                                               xml=to_xml))


if __name__ == '__main__':
    a = AXMLPrinter("test_apks/goatdroid.apksec")
    print a.start()
    # print get_from_to(r"D:\Store\document\all_my_work\CZY\ApkSec\test_apks\goatdroid.apksec", from_plugin="Unzip",
    #                   to_plugin="AXMLPrinter", magic="\x03\x00\x08\x00")
