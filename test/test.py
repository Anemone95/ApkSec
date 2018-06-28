#!/usr/bin/env python
# coding=utf-8

# @file test.py
# @brief 遍历test\android-apps-crawler\repo\apps文件夹，测试健壮性
# @author x565178035,x565178035@126.com
# @version 1.0
# @date 2018-06-01 16:08

import sys
import os

reload(sys)
sys.setdefaultencoding("utf-8")

SCRIPT_PATH = os.path.split(os.path.realpath(__file__))[0]
APPS_PATH = os.path.join(SCRIPT_PATH, 'android-apps-crawler', 'repo', 'apps')
APKSEC_PATH = os.path.join(SCRIPT_PATH, '..', 'mt_console.py')


def test_dir(apk_dir):
    for each_file in os.listdir(apk_dir):
        test_single(os.path.join(apk_dir, each_file))


def test_single(apk_path):
    path, name=os.path.split(apk_path)
    cmd='python {apksec} start -F {apkpath} -v -i Procyon 2>&1 | tee logs/{log}_std.log'.format(apksec=APKSEC_PATH, apkpath=apk_path, log=name)
    print cmd
    os.system(cmd)

if __name__ == '__main__':
    test_dir(APPS_PATH)
    #  test_single(os.path.join(APPS_PATH, '0fdef275053a381a9edf7f63fc9c4ca4.apk'))
