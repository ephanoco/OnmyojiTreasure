#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 17:00
# @Author  : Samuel
# @File    : realm_raider.py
import time

from modules.common.battle_concluder import BattleConcluder
from utils.matcher import Matcher
from utils.tmpl_dict import tmpl_dict


class RealmRaider:
    def __init__(self, matcher: Matcher, battle_concluder: BattleConcluder):
        self.matcher = matcher
        self.battle_concluder = battle_concluder
        self.dict_realm_raid = tmpl_dict['exploration']['realm_raid']
        self.guild_defeated_count = 0

    def raid(self, is_individual, is_cooldown=False, ran_out_cb=None):
        """

        :param is_individual:
        :param is_cooldown:Guild realm raid cooldown
        :param ran_out_cb:Individual realm raid passes ran out.
        :return:
        """
        # is_individual = len(super().match(
        #     super().get_path(f'{self.rel_path}individual_active.png'), thresh_mul=0.98
        # )) != 0
        self.__individual_raid(ran_out_cb=ran_out_cb) if is_individual else self.__guild_raid(is_cooldown)

    def __guild_raid(self, is_cooldown, index: str = ''):
        """

        :param is_cooldown: Realm raid cooldown
        :param index:
        :return:
        """
        # Choose the realm
        scatter = self.__get_scatter('guild')
        cur_index = self.guild_defeated_count if not index else int(index)
        self.matcher.left_click(scatter[cur_index], (1, 2))

        tmpl_raid = self.dict_realm_raid['raid']
        pt_raid_list = self.matcher.match(tmpl_raid['path'],
                                          thresh_mul=tmpl_raid['thresh_mul']) if not is_cooldown else [
            self.matcher.match(tmpl_raid['path'], is_multiple=tmpl_raid['is_multiple'],
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
                self.matcher.left_click(scatter[cur_index + 1], (1, 2))
                return self.__guild_raid(True, str(cur_index))
        self.matcher.left_click(pt_raid_list[0], 2)  # Raid
        # The realm has been raided
        pt_raid_list = self.matcher.match(tmpl_raid['path'],
                                          thresh_mul=tmpl_raid['thresh_mul'])
        if pt_raid_list:
            self.matcher.left_click(scatter[cur_index + 1], (1, 2))
            return self.__guild_raid(is_cooldown, str(cur_index + 1))

        time.sleep(2)
        self.__mark_ghost()

        def __vic_cb():
            self.__guild_raid(is_cooldown)

        def __def_cb():
            self.guild_defeated_count += 1
            if self.guild_defeated_count <= len(scatter):
                self.__guild_raid(is_cooldown)

        self.battle_concluder.conclude_battle(10, __vic_cb, def_cb=__def_cb)

    def __mark_ghost(self, pt=(), times=0):
        """

        :param pt:Shikigami coordinates
        :param times:Maximum mark times
        :return:
        """
        if times == 10:
            return
        pt_ghost = self.__get_pt_ghost() if not pt else pt
        self.matcher.left_click(pt_ghost, 0.4)
        self.matcher.capture()
        tmpl_mark = self.dict_realm_raid['mark']
        is_marked = len(self.matcher.match(tmpl_mark['path'], False,
                                           thresh_mul=tmpl_mark['thresh_mul'])) != 0
        print(f'is_marked: {is_marked}')
        if not is_marked:
            self.__mark_ghost(pt_ghost, times=times + 1)

    def __get_pt_ghost(self):
        """
        Get shikigami coordinates.
        :return:shikigami coordinates
        """
        cx, cy = self.__get_pt_nickname()
        time.sleep(1)
        return cx - 4, cy + 70

    def __get_pt_nickname(self):
        """
        Get Shikigami nickname coordinates.
        :return:Shikigami nickname coordinates
        """
        self.matcher.capture()
        tmpl_nickname = self.dict_realm_raid['nickname']
        pt_nickname_list = self.matcher.match(tmpl_nickname['path'], False,
                                              thresh_mul=tmpl_nickname['thresh_mul'])
        print(f'pt_nickname_list: {pt_nickname_list}')
        if pt_nickname_list:
            return pt_nickname_list[0]
        return self.__get_pt_nickname()

    def __get_scatter(self, mode):
        """

        :param mode: Guild or individual.
        :return:
        """
        scatter = self.dict_realm_raid[mode]['scatter']
        if not scatter:
            pt_realm_buffs = self.dict_realm_raid['realm_buffs']['pt']  # (230, 238)
            if not pt_realm_buffs:
                tmpl_buffs = self.dict_realm_raid['realm_buffs']
                pt_realm_buffs = self.dict_realm_raid['realm_buffs']['pt'] = self.matcher.match(tmpl_buffs['path'],
                                                                                                thresh_mul=tmpl_buffs[
                                                                                                    'thresh_mul'])[0]
            cx, cy = pt_realm_buffs
            scatter = self.dict_realm_raid[mode]['scatter'] = [(cx + 285, cy - 20), (cx + 551, cy - 20),
                                                               (cx + 816, cy - 20), (cx + 285, cy + 88),
                                                               (cx + 551, cy + 88), (cx + 816, cy + 88),
                                                               (cx + 285, cy + 196), (cx + 551, cy + 196),
                                                               (cx + 816, cy + 196)] if mode == 'individual' else [
                (cx + 437, cy + 34), (cx + 707, cy + 34), (cx + 437, cy + 142), (cx + 707, cy + 142),
                (cx + 437, cy + 250),
                (cx + 707, cy + 250), (cx + 437, cy + 299), (cx + 707, cy + 299)]
        print(f'scatter: {scatter}')
        return scatter

    def __individual_raid(self, index: str = '', ran_out_cb=None):
        """

        :param index:
        :param ran_out_cb:Realm raid passes ran out.
        :return:
        """
        # Choose the realm
        scatter = self.__get_scatter('individual')
        cur_index = 0 if not index else int(index)
        # Retreat two
        is_retreat_two = False
        if cur_index == 8:
            is_retreat_two = True
            self.__retreat_two(scatter)

        if not is_retreat_two:
        self.matcher.left_click(scatter[cur_index], (1, 2))

            tmpl_raid = self.dict_realm_raid['raid']
            pt_raid_list = self.matcher.match(tmpl_raid['path'], thresh_mul=tmpl_raid['thresh_mul'])
            print(f'pt_raid_list: {pt_raid_list}')
            # The realm has been raided
            if not pt_raid_list:
                return self.__individual_raid(str(cur_index + 1))
            self.matcher.left_click(pt_raid_list[0], 2)  # Raid
            pt_raid_list = self.matcher.match(tmpl_raid['path'], thresh_mul=tmpl_raid['thresh_mul'])
            # Passes ran out
            if pt_raid_list:
                if ran_out_cb:
                    ran_out_cb()
                return

            time.sleep(2)
        self.__mark_ghost()

        def __vic_cb():
            # Milestone handler
            if cur_index == 2 or cur_index == 5 or cur_index == 8:
                pt_vic = self.__get_rel_pt('realm_buffs', 'victory')
                time.sleep(1)
                self.matcher.left_click(pt_vic, (1, 2))  # XXX

            if cur_index < 8:
                self.__individual_raid(str(cur_index + 1))
            else:
                # Lock the lineup
                pt_lock = self.__get_rel_pt('realm_buffs', 'lock')
                self.matcher.left_click(pt_lock, (1, 2))

                self.__individual_raid()

        self.battle_concluder.conclude_battle(10, __vic_cb, False)

    def __retreat_two(self, scatter):
        # Unlock the lineup
        pt_lock = self.__get_rel_pt('realm_buffs', 'lock')
        self.matcher.left_click(pt_lock, (1, 2))
        self.matcher.left_click(scatter[-1], (1, 2))  # Choose the realm
        tmpl_raid = self.dict_realm_raid['raid']
        pt_raid = self.matcher.match(tmpl_raid['path'], thresh_mul=tmpl_raid['thresh_mul'])[0]
        print(f'pt_raid: {pt_raid}')
        self.matcher.left_click(pt_raid, 2)  # Raid
        pt_raid_list = self.matcher.match(tmpl_raid['path'], thresh_mul=tmpl_raid['thresh_mul'])
        # Passes ran out
        if pt_raid_list:
            return

        time.sleep(3)
        self.__get_pt_battle_buffs()  # Get ref pt
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
        tmpl_battle_buffs = self.dict_realm_raid['individual']['battle_buffs']
        if not pt_battle_buffs:
            pt_battle_buffs = self.dict_realm_raid['individual']['battle_buffs']['pt'] = \
                self.matcher.match(tmpl_battle_buffs['path'], thresh_mul=tmpl_battle_buffs['thresh_mul'])[0]
        print(f'pt_battle_buffs: {pt_battle_buffs}')
        return pt_battle_buffs

    def __get_rel_pt(self, ref, rel):
        """
        Compute relative coordinates based on reference coordinates.
        :param ref:The key of the reference coordinates.
        :param rel:The key of the relative coordinates.
        :return:Relative coordinates
        """
        dict_ref = {
            'realm_buffs': self.dict_realm_raid['realm_buffs']['pt'],
            'battle_buffs': self.dict_realm_raid['individual']['battle_buffs']['pt'],
        }
        cx, cy = dict_ref[ref]
        dict_rel = {
            'realm_buffs': {
                'lock': (cx + 609, cy + 333),
                'victory': (cx + 451, cy + 292),
            },
            'battle_buffs': {
                'return': (cx - 78, cy - 509),
                'confirm': (cx + 487, cy - 197),
                'retreat': (cx + 565, cy - 86),
                'prepare': (cx + 818, cy - 65),
            },
        }
        return dict_rel[ref][rel]


if __name__ == '__main__':
    matcher = Matcher()
    bc = BattleConcluder(matcher)
    realm_raider = RealmRaider(matcher, bc)
    realm_raider.raid(False)
