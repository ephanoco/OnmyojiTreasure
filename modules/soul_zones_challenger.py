#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/30 5:21
# @Author  : Samuel
# @File    : soul_zones_challenger.py
import time

from modules.common.battle_concluder import BattleConcluder
from modules.realm_raider import RealmRaider
from utils.tmpl_dict import tmpl_dict


class SoulZonesChallenger(BattleConcluder):
    def __init__(self):
        super().__init__()
        self.dict_exploration = tmpl_dict['exploration']
        self.count = 0

    def challenge_sougenbi(self, is_empty=False):
        """

        :param is_empty:Automatically empty realm raid passes.
        :return:
        """
        # Access Sougenbi
        pt_challenge = self.dict_exploration['soul_zones']['sougenbi']['challenge']['pt']
        tmpl_challenge = self.dict_exploration['soul_zones']['sougenbi']['challenge']
        if not pt_challenge:
            pt_challenge = self.dict_exploration['soul_zones']['sougenbi']['challenge']['pt'] = \
                super().match(tmpl_challenge['path'],
                              thresh_mul=tmpl_challenge['thresh_mul'])[0]
        super().left_click(pt_challenge, 2)

        pt_challenge_list = super().match(tmpl_challenge['path'],
                                          thresh_mul=tmpl_challenge['thresh_mul'])
        # Scrolls ran out
        if pt_challenge_list:
            return

        time.sleep(3)

        def vic_cb():
            if is_empty:
                # Empty realm raid passes
                self.count += 1
                '''
                150 = 30 / 20%
                Single drop rate 20%, team drop rate 21.6%.
                '''
                if self.count == 150:
                    self.__empty_passes(is_empty)

            self.challenge_sougenbi(is_empty)

        super().conclude_battle(39, vic_cb, False)  # first_loop_delay: 17

    def __empty_passes(self, is_empty):
        """
        Empty realm raid passes.
        :param is_empty: Automatically empty.
        :return:
        """
        # Return to the exploration
        pt_return = self.__get_rel_pt('challenge', 'return')
        super().left_click(pt_return, (1, 2))
        # Access the realm raid
        pt_realm_raid = self.dict_exploration['realm_raid_btn']['pt']
        tmpl_realm_raid = self.dict_exploration['realm_raid_btn']
        if not pt_realm_raid:
            pt_realm_raid = self.dict_exploration['realm_raid_btn']['pt'] = \
                super().match(tmpl_realm_raid['path'],
                              thresh_mul=tmpl_realm_raid['thresh_mul'])[0]
        super().left_click(pt_realm_raid, (1, 2))

        def ran_out_cb():
            # Return to the exploration
            pt_close = self.dict_exploration['realm_raid']['close']['pt']
            if not pt_close:
                pt_close = self.dict_exploration['realm_raid']['close']['pt'] = \
                    super().match(self.dict_exploration['realm_raid']['close']['path'])[0]
            super().left_click(pt_close, (1, 2))
            # Access Sougenbi
            pt_soul_zones_btn = self.__get_rel_pt('realm_raid_btn', 'soul_zones_btn')
            super().left_click(pt_soul_zones_btn, (1, 2))
            pt_sougenbi_btn = self.dict_exploration['soul_zones']['sougenbi_btn']['pt']
            if not pt_sougenbi_btn:
                pt_sougenbi_btn = self.dict_exploration['soul_zones']['sougenbi_btn']['pt'] = \
                    super().match(self.dict_exploration['soul_zones']['sougenbi_btn']['path'])[0]
            super().left_click(pt_sougenbi_btn, (1, 2))

        if is_empty:
            realm_raider = RealmRaider()
            realm_raider.raid(True, False, ran_out_cb)

    def __get_rel_pt(self, ref, rel):
        """
        Compute relative coordinates based on reference coordinates.
        :param ref:The key of the reference coordinates.
        :param rel:The key of the relative coordinates.
        :return:Relative coordinates
        """
        dict_ref = {
            'challenge': self.dict_exploration['soul_zones']['sougenbi']['challenge']['pt'],
            'realm_raid_btn': self.dict_exploration['realm_raid_btn']['pt'],
        }
        cx, cy = dict_ref[ref]
        dict_rel = {
            'challenge': {
                'return': (cx - 871, cy - 467),
            },
            'realm_raid_btn': {
                'soul_zones_btn': (cx - 84, cy + 3),
            },
        }
        return dict_rel[ref][rel]


if __name__ == '__main__':
    soul_zones_challenger = SoulZonesChallenger()
    soul_zones_challenger.challenge_sougenbi()
