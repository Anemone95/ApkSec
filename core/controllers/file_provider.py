#!/usr/bin/env python
# -*- coding=utf-8 -*-
import os
import re


class FileProvider(object):
    def __new__(cls, project_path, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(FileProvider, cls).__new__(cls, *args, **kwargs)
            cls._instance.files = {}
            cls._instance.project_path = project_path
        return cls._instance

    def get_files(self, unpacker, regex=None, magic=None):
        """

        :param unpacker: unpacker字符串名称，用来获取某个unpacker文件夹下的类型文件
        :param regex: 使用正则表达式搜索，建议使用原始字符串
        :param magic: 使用文件头的magic搜索，请使用字符串形式，如'\x03\x00\x08\x00'
        :return:
        """
        key = '{0}_{1}'.format(unpacker, regex if magic == None else magic)
        if key in self.files.keys():
            return self.files[key]
        else:
            res = []
            search_dir = os.path.join(self.project_path, unpacker)
            if regex:
                pattern = re.compile(regex)
                for root, dirs, files in os.walk(search_dir):
                    for f in files:
                        if pattern.match(f):
                            res.append(os.path.join(root, f))
            elif magic:
                for root, dirs, files in os.walk(search_dir):
                    for f in files:
                        file_path = os.path.join(root, f)
                        with open(file_path, 'r') as _file:
                            file_magic = _file.read(12)
                            if file_magic.startswith(magic):
                                res.append(file_path)

            self.files[key] = res
            return res


if __name__ == '__main__':
    fp = FileProvider(r'D:\Store\document\all_my_work\CZY\ApkSec\test_apks\goatdroid.apksec')
    print fp.get_files(unpacker='Unzip', magic="\x03\x00\x08\x00")
