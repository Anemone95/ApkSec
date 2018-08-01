#!/usr/bin/env python
# -*- coding=utf-8 -*-
import logging
import json

import os

import core.controllers.controller as ctrl


def start(path, log_level=logging.INFO):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(filename)s : %(funcName)s() : %(message)s',
                        level=log_level)
    res = ctrl.start(path)
    res = map(lambda e: e.to_dict(), res)
    return json.dumps(res)


def stop(apk_name):
    cmd = 'ps -ef|grep -E "start -F.{}.apk|PID"'.format(apk_name)
    ps_res = os.popen(cmd).readlines()
    flags = ps_res[0].split()
    pid_idx = flags.index("PID")
    for each_line in ps_res[1:]:
        pid = each_line.split()[pid_idx]
        kill_res = os.popen("kill {}".format(pid))


if __name__ == '__main__':
    print start('../../test_apks/goatdroid.apk', log_level=logging.DEBUG)
