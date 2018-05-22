#!/usr/bin/env python
# -*- coding=utf-8 -*-

import core.controllers.plugin_category as plugin_category
from core.controllers.const import *
from core.controllers.utils import *
from settings import *


class Template(plugin_category.Unpacker):
    def __init__(self, task_path=None):
        plugin_category.Unpacker.__init__(self)
        """do something"""

    def _dependencies(self):
        return []

    def _ability(self):
        return {}

    def start(self):
        """do something"""
