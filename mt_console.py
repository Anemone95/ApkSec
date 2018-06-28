#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""Usage:
mt_console start -F <apk_dir> [-v] [-i <ignore-plugins>] [--skip-unpacker]
mt_console stop
mt_console bash
mt_console (-h|--help)

Options:
  -h --help      Show this screen.
  start:         Start a scan.
      -v                Verbose log.
      -d                Debug log.
      --skip-unpacker   Skip unpacker (just for debug).
  stop          Stop a scan.
  bash          start a bash.
"""
import json
import logging
import os
import shutil
import subprocess

import time
from docopt import docopt

import core.controllers.controller as ctrl


def _format(dic):
    """
    格式化返回格式，符合慕测要求
    :param dic:
    :return:
    """
    # 修改一下reference的字段名
    references = map(lambda ref: {'location': ref['location'], 'description': ref['detail']}, dic['reference'])

    # 修改一个vuln的格式
    return dict(name=dic['vulnerability']['i18n_name'],
                updateTime=dic['update_time'],
                description=dic['vulnerability']['description'],
                vulType=0,
                riskLevel=dic['vulnerability']['risk_level'] + 1,
                targetTaskId=0,
                solution=dic['vulnerability']['solution'],
                source='android_apk',
                vulReferences=references)


def start(path, ignore_plugins, log_level=logging.INFO, skip_unpacker=False):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(filename)s : %(funcName)s() : %(message)s',
                        level=log_level)
    res = ctrl.start(path, skip_unpacker=skip_unpacker, ignore_plugins=ignore_plugins)
    res = filter(lambda vulns: vulns.reference, res)
    res = map(lambda e: _format(e.to_dict()), res)
    print json.dumps(res)


def stop():
    files = os.listdir('.')
    rmfiles = []
    for filename in files:
        if filename.endswith('.apksec'):
            apk_name = filename.split('.')[0]
            cmd = 'ps -ef|grep -E "start -F.*{}.apk|PID"'.format(apk_name)
            ps_res = os.popen(cmd).readlines()
            flags = ps_res[0].split()
            pid_idx = flags.index("PID")
            for each_line in ps_res[1:]:
                pid = each_line.split()[pid_idx]
                if 'grep' not in each_line:
                    cmd = "kill {}".format(pid)
                    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout, stderr = process.communicate()
                    if process.returncode:
                        raise Exception(stderr)
            rmfiles.append(filename)

    for each in rmfiles:
        if os.path.exists(os.path.join('.', each)):
            failed = True
            while failed:
                try:
                    shutil.rmtree(os.path.join('.', each))
                    failed = False
                except OSError as e:
                    logging.error(e)
                time.sleep(1)
                logging.error('Retry after 1 seconds.')
    logging.info('Stop success.')


def main():
    arguments = docopt(__doc__, version='1.0.0')
    if arguments["start"]:
        if arguments["-v"]:
            log_level = logging.DEBUG
        else:
            log_level = logging.ERROR
        if arguments["-i"]:
            ignore_plugins = arguments["<ignore-plugins>"].split(',')
        else:
            ignore_plugins = []
        if arguments["--skip-unpacker"]:
            skip_unpacker = True
        else:
            skip_unpacker = False
        start(arguments["<apk_dir>"], log_level=log_level, skip_unpacker=skip_unpacker, ignore_plugins=ignore_plugins)
    elif arguments["stop"]:
        stop()
    elif arguments["bash"]:
        os.system("bash")


if __name__ == '__main__':
    main()
