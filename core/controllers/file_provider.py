#!/usr/bin/env python
# -*- coding=utf-8 -*-
import logging
import re

import apksec_exceptions
from core.controllers.decorator import singleton


@singleton
class FileProvider(object):
    def __init__(self):
        self.files = {}
        self.unpackers = []

    def register_unpacker(self, unpacker):
        logging.info("Unpacker: {} registered.".format(unpacker))
        self.unpackers.append(unpacker)

    def get_files(self, unpacker_name, regex=None, magic=None):
        """

        :param unpacker_name: unpacker.name，用来获取某个unpacker文件夹下的类型文件
        :param regex: 使用正则表达式搜索，带路径，建议使用原始字符串
        :param magic: 使用文件头的magic搜索，请使用字符串形式，如'\x03\x00\x08\x00'
        :return:
        """
        unpacker = None
        for each_unpacker in self.unpackers:
            if each_unpacker.plugin_name == unpacker_name:
                unpacker = each_unpacker
                break
        if not unpacker:
            err_str = "Unpacker: '{}' not in registered unpackers.".format(unpacker_name)
            logging.error(err_str)
            raise apksec_exceptions.FileProviderException(err_str)
        # 缓存机制
        key = '{0}_{1}_{2}'.format(unpacker.plugin_name, regex, magic)
        if key in self.files.keys():
            return self.files[key]

        res = []
        if regex:
            pattern = re.compile(regex)
            only_java = True if regex.endswith('java') else False
            for file_path in unpacker.success_files(only_java):
                if pattern.match(file_path):
                    res.append(file_path)
        if magic:
            if len(res) == 0:
                for file_path in unpacker.success_files():
                    with open(file_path, 'r') as _file:
                        file_magic = _file.read(12)
                        if file_magic.startswith(magic):
                            res.append(file_path)
            else:
                filtered_res = []
                for file_path in res:
                    with open(file_path, 'r') as _file:
                        file_magic = _file.read(12)
                        if file_magic.startswith(magic):
                            filtered_res.append(file_path)
                res = filtered_res

        self.files[key] = res
        return res

    def get_files_by_type(self, file_type):
        """
        选择一个恰当的unpacker并返回其结果
        :param file_type:
        :return:
        """
        unpackers = filter(lambda e: file_type in e.ability.keys(), self.unpackers)
        # 寻找能力最强的解包器
        unpackers.sort(key=lambda e: -e.ability[file_type].value)
        for each_unpacker in unpackers:
            if len(each_unpacker.failed_files.get(file_type, {})) == 0:
                return self.get_files(each_unpacker.plugin_name,
                                      regex=".*"+file_type.value["filename"],
                                      magic=file_type.value["magic"])
        return self.get_files(unpackers[0].plugin_name,
                              regex=".*"+file_type.value["filename"],
                              magic=file_type.value["magic"])


if __name__ == '__main__':
    fp = FileProvider()
