#!/usr/bin/env python
# -*- coding=utf-8 -*-

import sys
import gettext as gt
import os

reload(sys)
sys.setdefaultencoding("utf-8")


def lgettext(domain_name, coding='utf-8'):
    language_dir = os.path.split(os.path.realpath(__file__))[0]
    gt.bindtextdomain(domain_name, language_dir)
    gt.bind_textdomain_codeset(domain_name, coding)
    gt.textdomain(domain_name)
    return gt.lgettext


def gettext(domain_name):
    language_dir = os.path.split(os.path.realpath(__file__))[0]
    gt.bindtextdomain(domain_name, language_dir)
    gt.textdomain(domain_name)
    return gt.gettext


def ugettext(domain_name):
    '''
    返回Unicode字符串，推荐使用，需要安装语言包
    :param domain_name:
    :return:
    '''
    language_dir = os.path.split(os.path.realpath(__file__))[0]
    try:
        t = gt.translation(domain_name, language_dir)
    except IOError:
        return gettext(domain_name)
    return t.ugettext


if __name__ == '__main__':
    pass
