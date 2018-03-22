#!/usr/bin/env python
# -*- coding=utf-8 -*-

import logging
import core.controllers.ctrl_main as ctrl

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(filename)s : %(funcName)s() : %(message)s',
                        level=logging.INFO)
    ctrl.start('test_apks/goatdroid.apk')