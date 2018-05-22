#!/usr/bin/env python
# -*- coding=utf-8 -*-
import zipfile

import core.controllers.plugin_category as plugin_category
from core.controllers.const import *


class Unzip(plugin_category.Unpacker):
    def _ability(self):
        return {TYPE.DEX: ABILITY.C,
                TYPE.ELF: ABILITY.C}

    def start(self):
        zip_file = zipfile.ZipFile(self.apk_path)
        zip_file.extractall(path=self.plugin_task_path)


if __name__ == '__main__':
    pass
