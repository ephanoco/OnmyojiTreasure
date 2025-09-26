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
from modules.common.battle_concluder import BattleConcluder
from utils.matcher import Matcher


class OnmyojiTreasure:
    def __init__(self):
        self.matcher = Matcher()
        self.battle_concluder = BattleConcluder(self.matcher)
        self.realm_raider = RealmRaider(self.matcher, self.battle_concluder)
        self.beans_thrower = BeansThrower(self.matcher)
        self.soul_zones = SoulZonesChallenger(self.matcher, self.battle_concluder, self.realm_raider)

    def start(self):
        modes = {'1': 'Realm Raid (结界突破)', '2': 'Demon Parade (百鬼夜行)', '3': 'Soul Zones (御魂)'}
        choice = self.matcher.query_mode(modes)
        if choice == '1':
            is_individual = self.matcher.query_yes_no("Is individual?")
            is_cooldown = False
            if not is_individual:
                is_cooldown = self.matcher.query_yes_no("Is cooldown?")
            self.realm_raider.raid(is_individual, is_cooldown)
        elif choice == '2':
            self.beans_thrower.throw_beans()
        elif choice == '3':
            soul_zones = {'1': 'Orochi (八岐大蛇)', '2': 'Sougenbi (业原火)', '3': 'Fallen Sun (日轮之陨)',
                          '4': 'Sea of Eternity (永生之海)'}
            soul_zone = self.matcher.query_mode(soul_zones)
            if soul_zone == '1':
                pass
            elif soul_zone == '2':
                is_empty = self.matcher.query_yes_no("Is automatically empty realm raid passes?")
                self.soul_zones.challenge_sougenbi(is_empty)
            elif soul_zone == '3':
                pass
            elif soul_zone == '4':
                pass


def is_admin():
    """
    Determine if obtained admin rights.
    :return:
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    tr = OnmyojiTreasure()
    tr.start()
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None,
                                        1)  # Re-run the program with admin rights
