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
    XML = 1
    ELF = 2
    DEX = '.dex'
    SMALI = 4
    JAVA = '.java'
    JAR = '.jar'
    MANIFEST = 'AndroidManifest.xml'
    APK = 'backup.apk'
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
