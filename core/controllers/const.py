#!/usr/bin/env python
# -*- coding=utf-8 -*-
from enum import unique, Enum

WINDOWS = "WindowsPE"
LINUX = "ELF"
X86 = "32bit"
X64 = " 64bit"


@unique
class TYPE(Enum):
    AXML = 0
    XML = {"filename": ".xml", "magic": "\x3c\x3f\x78\x6d\x6c"}
    ELF = 2
    DEX = '.dex'
    SMALI = 4
    JAVA = {"filename": ".java", "magic": None}
    JAR = {"filename": ".jar", "magic": None}
    MANIFEST = {
        "filename": "AndroidManifest.xml",
        "magic": "\x3c\x3f\x78\x6d\x6c"}
    APK = {"filename": ".apk", "magic": None}
    JAVA_CLASS = 5


@unique
class ABILITY(Enum):
    E = 0
    D = 1
    C = 2
    B = 3
    A = 4


@unique
class RISK(Enum):
    INFO = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
