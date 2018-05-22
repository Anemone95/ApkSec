#!/usr/bin/env python
# -*- coding=utf-8 -*-

import core.controllers.plugin_category as plugin_category
from core.controllers.const import *
from core.controllers.utils import *
from settings import *


class JavaCollector(plugin_category.Unpacker):
    def __init__(self, task_path=None):
        plugin_category.Unpacker.__init__(self)
        """do something"""

    def _dependencies(self):
        return TYPE.JAVA

    def _ability(self):
        return {TYPE.JAVA: ABILITY.A}

    def start(self):
        """do something"""
        assert os.path.exists(os.path.join(self.plugin_task_path, "..", "CFR", "summary.txt"))
