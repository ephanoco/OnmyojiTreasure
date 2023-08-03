#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/30 5:21
# @Author  : Samuel
# @File    : soul_zones_challenger.py
import time

from modules.common.battle_concluder import BattleConcluder
from utils.tmpl_dict import tmpl_dict


class SoulZonesChallenger(BattleConcluder):
    def __init__(self):
        super().__init__()
        self.dict_soul_zones = tmpl_dict['exploration_map']['soul_zones']

    def challenge_sougenbi(self):
        pt_challenge = self.dict_soul_zones['sougenbi']['challenge']['pt']
        tmpl_challenge = self.dict_soul_zones['sougenbi']['challenge']
        if not pt_challenge:
            pt_challenge = self.dict_soul_zones['sougenbi']['challenge']['pt'] = \
                super().match(tmpl_challenge['path'],
                              thresh_mul=tmpl_challenge['thresh_mul'])[0]
        super().left_click(pt_challenge, 2)
        pt_challenge_list = super().match(tmpl_challenge['path'],
                                          thresh_mul=tmpl_challenge['thresh_mul'])
        # Scrolls ran out
        if pt_challenge_list:
            return

        time.sleep(3)
        super().conclude_battle(39, lambda: self.challenge_sougenbi)  # first_loop_delay: 17


if __name__ == '__main__':
    soul_zones_challenger = SoulZonesChallenger()
    soul_zones_challenger.challenge_sougenbi()
