#!/usr/bin/env python
# -*- coding=utf-8 -*-
import zipfile

import core.controllers.plugin_category as plugin_category


class Unzip(plugin_category.Unpacker):

    def start(self):
        zip_file = zipfile.ZipFile(self.apk_path)
        zip_file.extractall(path=self.plugin_path)


if __name__ == '__main__':
    pass