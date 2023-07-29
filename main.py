#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 17:05
# @Author  : Samuel
# @File    : main.py
import ctypes
import sys

from modules.beans_thrower import BeansThrower
from modules.realm_raider import RealmRaider
from modules.soul_zones_challenger import SoulZonesChallenger


class OnmyojiTreasure(RealmRaider, BeansThrower, SoulZonesChallenger):
    def start(self):
        if super().is_admin():
            modes = {'1': 'Realm Raid (结界突破)', '2': 'Demon Parade (百鬼夜行)', '3': 'Soul Zones (御魂)'}
            choice = super().query_mode(modes)
            if choice == '1':
                is_individual = super().query_yes_no("Is individual?")
                is_cooldown = False
                if not is_individual:
                    is_cooldown = super().query_yes_no("Is cooldown?")
                super().raid(is_individual, is_cooldown)
            elif choice == '2':
                super().throw_beans()
            elif choice == '3':
                soul_zones = {'1': 'Orochi (八岐大蛇)', '2': 'Sougenbi (业原火)', '3': 'Fallen Sun (日轮之陨)',
                              '4': 'Sea of Eternity (永生之海)'}
                soul_zone = super().query_mode(soul_zones)
                if soul_zone == '1':
                    pass
                elif soul_zone == '2':
                    super().challenge_sougenbi()
                elif soul_zone == '3':
                    pass
                elif soul_zone == '4':
                    pass
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None,
                                                1)  # Re-run the program with admin rights


tr = OnmyojiTreasure()
tr.start()
