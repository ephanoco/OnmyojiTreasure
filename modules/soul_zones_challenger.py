#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/30 5:21
# @Author  : Samuel
# @File    : soul_zones_challenger.py
import time

from utils.matcher import Matcher
from utils.pt_dict import pt_dict


class SoulZonesChallenger(Matcher):
    def __init__(self):
        super().__init__()
        self.rel_path = 'static/templates/exploration_map/soul_zones/sougenbi/'

    def challenge_sougenbi(self):
        pt_challenge = pt_dict['exploration_map']['soul_zones']['sougenbi']['challenge']
        if not pt_challenge:
            pt_challenge = pt_dict['exploration_map']['soul_zones']['sougenbi']['challenge'] = super().match(
                super().get_path(f'{self.rel_path}challenge.png'))[0]
        super().left_click(pt_challenge, 2)
        pt_challenge = super().match(
            super().get_path(f'{self.rel_path}challenge.png'))[0]
        # Scrolls ran out
        if pt_challenge:
            return

        time.sleep(3)
        is_first_loop = True
        while True:
            if is_first_loop:
                time.sleep(39)  # 17
                is_first_loop = False
            else:
                time.sleep(1)
            super().capture()
            pt_victory_list = super().match(super().get_path(f'{self.rel_path}victory.png'), False, thresh_mul=0.96)
            if pt_victory_list:
                time.sleep(1)
                super().left_click(pt_victory_list[0], (4, 5))
                self.challenge_sougenbi()
                break
            pt_defeat_list = super().match(super().get_path(f'{self.rel_path}defeat.png'), False)
            if pt_defeat_list:
                return


if __name__ == '__main__':
    soul_zones_challenger = SoulZonesChallenger()
    soul_zones_challenger.challenge_sougenbi()
