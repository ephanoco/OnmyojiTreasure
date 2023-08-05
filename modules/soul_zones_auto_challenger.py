#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/6 1:30
# @Author  : Samuel
# @File    : soul_zones_auto_challenger.py
from modules.realm_raider import RealmRaider
from modules.soul_zones_challenger import SoulZonesChallenger
from utils.tmpl_dict import tmpl_dict


class SoulZonesAutoChallenger(SoulZonesChallenger, RealmRaider):
    def __init__(self):
        super().__init__()
        self.count = 0
        self.dict_exploration = tmpl_dict['exploration']

    def auto_challenge_sougenbi(self):
        super().challenge_sougenbi(self.vic_cb)

    def vic_cb(self):
        # Empty realm raid passes
        self.count += 1
        '''
        150 = 30 / 20%
        Single drop rate 20%, team drop rate 21.6%.
        '''
        if self.count == 150:
            self.__empty_passes()

        super().challenge_sougenbi(self.vic_cb)

    def __empty_passes(self):
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

            self.auto_challenge_sougenbi()

        super().raid(True, False, ran_out_cb)

    def __get_rel_pt(self, base, rel):
        dict_base = {
            'challenge': self.dict_exploration['soul_zones']['sougenbi']['challenge']['pt'],
            'realm_raid_btn': self.dict_exploration['realm_raid_btn']['pt'],
        }
        x, y = dict_base[base]
        dict_rel = {
            'challenge': {
                'return': (x - 871, y - 467),
            },
            'realm_raid_btn': {
                'soul_zones_btn': (x - 84, y + 3),
            },
        }
        return dict_rel[base][rel]
