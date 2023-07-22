#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 17:05
# @Author  : Samuel
# @File    : main.py
import ctypes
import sys

from modules.realm_raider import RealmRaider


class OnmyojiTreasure(RealmRaider):
    pass


onmyoji_treasure = OnmyojiTreasure()
if onmyoji_treasure.is_admin():
    onmyoji_treasure.raid()
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None,
                                        1)  # Re-run the program with admin rights
