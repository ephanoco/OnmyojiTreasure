#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 17:00
# @Author  : Samuel
# @File    : realm_raider.py
import time

from modules.common.battle_concluder import BattleConcluder
from utils.tmpl_dict import tmpl_dict


class RealmRaider(BattleConcluder):
    def __init__(self):
        super().__init__()
        self.dict_realm_raid = tmpl_dict['exploration']['realm_raid']
        self.guild_defeated_count = 0

    def raid(self, is_individual, is_cooldown=False, ran_out_cb=None):
        # is_individual = len(super().match(
        #     super().get_path(f'{self.rel_path}individual_active.png'), thresh_mul=0.98
        # )) != 0
        self.__individual_raid(ran_out_cb=ran_out_cb) if is_individual else self.__guild_raid(is_cooldown)

    def __guild_raid(self, is_cooldown, index: str = ''):
        # Choose the realm
        scatter = self.__get_scatter('guild')
        cur_index = self.guild_defeated_count if not index else int(index)
        super().left_click(scatter[cur_index], (1, 2))

        tmpl_raid = self.dict_realm_raid['raid']
        pt_raid_list = super().match(tmpl_raid['path'],
                                     thresh_mul=tmpl_raid['thresh_mul']) if not is_cooldown else [
            super().match(tmpl_raid['path'], is_multiple=tmpl_raid['is_multiple'],
                          thresh_sgl=tmpl_raid['thresh_sgl'],
                          is_with_colour=tmpl_raid['is_with_colour'])]
        print(f'pt_raid_list: {pt_raid_list}')
        if not is_cooldown:
            # Successful penetration
            if not pt_raid_list:
                return
        else:
            # Cooldown
            if not pt_raid_list[0]:
                time.sleep(1800)
                super().left_click(scatter[cur_index + 1], (1, 2))
                return self.__guild_raid(True, str(cur_index))
        super().left_click(pt_raid_list[0], 2)  # Raid
        # The realm has been raided
        pt_raid_list = super().match(tmpl_raid['path'],
                                     thresh_mul=tmpl_raid['thresh_mul'])
        if pt_raid_list:
            super().left_click(scatter[cur_index + 1], (1, 2))
            return self.__guild_raid(is_cooldown, str(cur_index + 1))

        time.sleep(3)
        self.__mark_ghost()

        def __vic_cb():
            self.__guild_raid(is_cooldown)

        def __def_cb():
            self.guild_defeated_count += 1
            if self.guild_defeated_count <= len(scatter):
                self.__guild_raid(is_cooldown)

        super().conclude_battle(10, __vic_cb, def_cb=__def_cb)

    def __mark_ghost(self, pt=(), times=0):
        if times == 10:
            return
        pt_ghost = self.__get_pt_ghost() if not pt else pt
        super().left_click(pt_ghost, 0.4)
        super().capture()
        tmpl_mark = self.dict_realm_raid['mark']
        is_marked_light = len(super().match(tmpl_mark['path'], False,
                                            thresh_mul=tmpl_mark['thresh_mul'])) != 0
        print(f'is_marked[light]: {is_marked_light}')
        if is_marked_light:
            is_marked = True
        else:
            tmpl_mark_dark = self.dict_realm_raid['mark_dark']
            is_marked = (len(
                super().match(tmpl_mark_dark['path'], False,
                              thresh_mul=tmpl_mark_dark['thresh_mul'])) != 0)
            print(f'is_marked[dark]: {is_marked}')
        if not is_marked:
            self.__mark_ghost(pt_ghost, times=times + 1)

    def __get_pt_ghost(self):
        x, y = self.__get_pt_nickname()
        return x + 6, y + 74

    def __get_pt_nickname(self):
        super().capture()
        tmpl_nickname = self.dict_realm_raid['nickname']
        pt_nickname_light_list = super().match(tmpl_nickname['path'], False,
                                               thresh_mul=tmpl_nickname['thresh_mul'])
        print(f'pt_nickname_list[light]: {pt_nickname_light_list}')
        if pt_nickname_light_list:
            return pt_nickname_light_list[0]
        tmpl_nickname_dark = self.dict_realm_raid['nickname_dark']
        pt_nickname_dark_list = super().match(tmpl_nickname_dark['path'], False,
                                              thresh_mul=tmpl_nickname_dark['thresh_mul'])
        print(f'pt_nickname_list[dark]: {pt_nickname_dark_list}')
        if pt_nickname_dark_list:
            return pt_nickname_dark_list[0]
        time.sleep(0.2)  # XXX
        return self.__get_pt_nickname()

    def __get_scatter(self, mode):
        scatter = self.dict_realm_raid[mode]['scatter']
        if not scatter:
            pt_realm_buffs = self.dict_realm_raid['realm_buffs']['pt']  # (230, 238)
            if not pt_realm_buffs:
                tmpl_buffs = self.dict_realm_raid['realm_buffs']
                pt_realm_buffs = self.dict_realm_raid['realm_buffs']['pt'] = super().match(tmpl_buffs['path'],
                                                                                           thresh_mul=tmpl_buffs[
                                                                                               'thresh_mul'])[0]
            x, y = pt_realm_buffs
            scatter = self.dict_realm_raid[mode]['scatter'] = [(x + 285, y - 20), (x + 551, y - 20),
                                                               (x + 816, y - 20), (x + 285, y + 88),
                                                               (x + 551, y + 88), (x + 816, y + 88),
                                                               (x + 285, y + 196), (x + 551, y + 196),
                                                               (x + 816, y + 196)] if mode == 'individual' else [
                (x + 437, y + 34), (x + 707, y + 34), (x + 437, y + 142), (x + 707, y + 142),
                (x + 437, y + 250),
                (x + 707, y + 250), (x + 437, y + 299), (x + 707, y + 299)]
        print(f'scatter: {scatter}')
        return scatter

    def __individual_raid(self, index: str = '', ran_out_cb=None):
        # Choose the realm
        scatter = self.__get_scatter('individual')
        cur_index = 0 if not index else int(index)
        # Retreat two
        is_retreat_two = False
        if cur_index == 8:
            is_retreat_two = True
            self.__retreat_two(scatter)

        if not is_retreat_two:
            super().left_click(scatter[cur_index], (1, 2))

            tmpl_raid = self.dict_realm_raid['raid']
            pt_raid_list = super().match(tmpl_raid['path'], thresh_mul=tmpl_raid['thresh_mul'])
            print(f'pt_raid_list: {pt_raid_list}')
            # The realm has been raided
            if not pt_raid_list:
                return self.__individual_raid(str(cur_index + 1))
            super().left_click(pt_raid_list[0], 2)  # Raid
            pt_raid_list = super().match(tmpl_raid['path'], thresh_mul=tmpl_raid['thresh_mul'])
            # Passes ran out
            if pt_raid_list:
                if ran_out_cb:
                    ran_out_cb()
                return

            time.sleep(3)
        self.__mark_ghost()

        def __vic_cb():
            # Milestone handler
            if cur_index == 2 or cur_index == 5 or cur_index == 8:
                pt_vic = self.__get_rel_pt('realm_buffs', 'victory')
                time.sleep(1)
                super(RealmRaider, self).left_click(pt_vic, (1, 2))  # XXX

            if cur_index < 8:
                self.__individual_raid(str(cur_index + 1))
            else:
                # Lock the lineup
                pt_lock = self.__get_rel_pt('realm_buffs', 'lock')
                super(RealmRaider, self).left_click(pt_lock, (1, 2))

                self.__individual_raid()

        super().conclude_battle(10, __vic_cb, False)

    def __retreat_two(self, scatter):
        # Unlock the lineup
        pt_lock = self.__get_rel_pt('realm_buffs', 'lock')
        super().left_click(pt_lock, (1, 2))
        super().left_click(scatter[-1], (1, 2))  # Choose the realm
        tmpl_raid = self.dict_realm_raid['raid']
        pt_raid = super().match(tmpl_raid['path'], thresh_mul=tmpl_raid['thresh_mul'])[0]
        print(f'pt_raid: {pt_raid}')
        super().left_click(pt_raid, 2)  # Raid
        pt_raid_list = super().match(tmpl_raid['path'], thresh_mul=tmpl_raid['thresh_mul'])
        # Passes ran out
        if pt_raid_list:
            return

        time.sleep(3)
        self.__get_pt_battle_buffs()  # Get base pt
        pt_return = self.__get_rel_pt('battle_buffs', 'return')
        pt_confirm = self.__get_rel_pt('battle_buffs', 'confirm')
        pt_retreat = self.__get_rel_pt('battle_buffs', 'retreat')
        for i in range(2):
            super().left_click(pt_return, (1, 2))
            super().left_click(pt_confirm, (1, 2))  # XXX
            super().left_click(pt_retreat, (1, 2))
            super().left_click(pt_confirm, (5, 6))
        pt_prepare = self.__get_rel_pt('battle_buffs', 'prepare')
        super().left_click(pt_prepare, (1, 2))

    def __get_pt_battle_buffs(self):
        pt_battle_buffs = self.dict_realm_raid['individual']['battle_buffs']['pt']
        if not pt_battle_buffs:
            pt_battle_buffs = self.dict_realm_raid['individual']['battle_buffs']['pt'] = \
                super().match(self.dict_realm_raid['individual']['battle_buffs']['path'])[0]
        print(f'pt_battle_buffs: {pt_battle_buffs}')
        return pt_battle_buffs

    def __get_rel_pt(self, base, rel):
        dict_base = {
            'realm_buffs': self.dict_realm_raid['realm_buffs']['pt'],
            'battle_buffs': self.dict_realm_raid['individual']['battle_buffs']['pt'],
        }
        x, y = dict_base[base]
        dict_rel = {
            'realm_buffs': {
                'lock': (x + 609, y + 333),
                'victory': (x + 451, y + 292),
            },
            'battle_buffs': {
                'return': (x - 78, y - 509),
                'confirm': (x + 487, y - 197),
                'retreat': (x + 565, y - 86),
                'prepare': (x + 818, y - 65),
            },
        }
        return dict_rel[base][rel]


if __name__ == '__main__':
    realm_raider = RealmRaider()
    realm_raider.raid(True)
