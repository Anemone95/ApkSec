#!/usr/bin/env python
# -*- coding=utf-8 -*-

import os
import logging
from core.controllers.file_provider import FileProvider

def get_from_to(project_path, from_plugin, to_plugin, regex=None, magic=None):
    fp = FileProvider(project_path)
    ret = []
    if regex:
        files = fp.get_files(unpacker=from_plugin, regex=regex)
    else:
        files = fp.get_files(unpacker=from_plugin, magic=magic)
    for f in files:
        relative_path = f.split(from_plugin)[1].split(os.path.sep)
        to_path = os.path.join(project_path, to_plugin, *relative_path)
        ret.append((f, to_path))
    return ret

def download(url, file_path, file_name):
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    jar_path = os.path.join(file_path, file_name)
    if not os.path.exists(jar_path):
        logging.info("{0} not exist. Try to download from {1}.".format(file_name, url))
        stat = os.system("curl -L -o {1} {0}".format(url, jar_path))
        if stat != 0:
            logging.error("Download failed.")
            return False, jar_path
    return True, jar_path


if __name__ == '__main__':
    pass