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
        self.dot_path = 'exploration_map.realm_raid'
        self.guild_defeated_count = 0

    def raid(self, is_individual, is_cooldown):
        # is_individual = len(super().match(
        #     super().get_path(f'{self.rel_path}individual_active.png'), thresh_mul=0.98
        # )) != 0
        self.__individual_raid() if is_individual else self.__guild_raid(is_cooldown)

    def __guild_raid(self, is_cooldown, index: str = ''):
        # Choose the realm
        scatter = self.__get_scatter(2)
        cur_index = self.guild_defeated_count if not index else int(index)
        super().left_click(scatter[cur_index], (1, 2))

        tmpl_raid = super().get_val(tmpl_dict, f'{self.dot_path}raid')
        pt_raid_list = super().match(tmpl_raid['path'],
                                     thresh_mul=tmpl_raid['thresh_mul']) if not is_cooldown else [
            super().match(tmpl_raid['path'], is_multiple=tmpl_raid['is_multiple'], thresh_sgl=tmpl_raid['thresh_sgl'],
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
                return self.__guild_raid(True)
        super().left_click(pt_raid_list[0], 2)  # Raid
        # The realm has been raided
        pt_raid_list = super().match(tmpl_raid['path'], thresh_mul=tmpl_raid['thresh_mul'])
        if pt_raid_list:
            super().left_click(scatter[cur_index + 1], (1, 2))
            return self.__guild_raid(is_cooldown, str(cur_index + 1))

        time.sleep(3)
        self.__mark_ghost()

        def def_cb():
            self.guild_defeated_count += 1
            if self.guild_defeated_count <= len(scatter):
                self.__guild_raid(is_cooldown)

        super().conclude_battle(10, lambda: self.__guild_raid(is_cooldown), def_cb)

    def __mark_ghost(self, pt=(), times=0):
        if times == 10:
            return
        pt_ghost = self.__get_pt_ghost() if not pt else pt
        super().left_click(pt_ghost, 0.4)
        super().capture()
        tmpl_mark = super().get_val(tmpl_dict, f'{self.dot_path}.mark')
        is_marked_light = len(super().match(tmpl_mark['path'], False, thresh_mul=tmpl_mark['thresh_mul'])) != 0
        print(f'is_marked[light]: {is_marked_light}')
        if is_marked_light:
            is_marked = True
        else:
            tmpl_mark_dark = super().get_val(tmpl_dict, f'{self.dot_path}.mark_dark')
            is_marked = (len(
                super().match(tmpl_mark_dark['path'], False, thresh_mul=tmpl_mark_dark['thresh_mul'])) != 0)
            print(f'is_marked[dark]: {is_marked}')
        if not is_marked:
            self.__mark_ghost(pt_ghost, times=times + 1)

    def __get_pt_ghost(self):
        x, y = self.__get_pt_nickname()
        return x + 6, y + 74

    def __get_pt_nickname(self):
        super().capture()
        tmpl_nickname = super().get_val(tmpl_dict, f'{self.dot_path}.nickname')
        pt_nickname_light_list = super().match(tmpl_nickname['path'], False, thresh_mul=tmpl_nickname['thresh_mul'])
        print(f'pt_nickname_list[light]: {pt_nickname_light_list}')
        if pt_nickname_light_list:
            return pt_nickname_light_list[0]
        tmpl_nickname_dark = super().get_val(tmpl_dict, f'{self.dot_path}.nickname_dark')
        pt_nickname_dark_list = super().match(tmpl_nickname_dark['path'], False,
                                              thresh_mul=tmpl_nickname_dark['thresh_mul'])
        print(f'pt_nickname_list[dark]: {pt_nickname_dark_list}')
        if pt_nickname_dark_list:
            return pt_nickname_dark_list[0]
        time.sleep(0.2)  # XXX
        return self.__get_pt_nickname()

    def __get_scatter(self, mode):
        scatter_path = f'{self.dot_path}.{"individual" if mode == 1 else "guild"}.scatter'
        scatter = super().get_val(tmpl_dict, scatter_path)
        if not scatter:
            pt_buffs_path = f'{self.dot_path}.buffs.pt'
            pt_buffs = super().get_val(tmpl_dict, pt_buffs_path)  # (230, 238)
            if not pt_buffs:
                tmpl_buffs = super().get_val(tmpl_dict, f'{self.dot_path}.buffs')
                super().set_val(tmpl_dict, pt_buffs_path,
                                super().match(tmpl_buffs['path'],
                                              thresh_mul=tmpl_buffs['thresh_mul'])[0])
                pt_buffs = super().get_val(tmpl_dict, pt_buffs_path)
            x, y = pt_buffs
            super().set_val(tmpl_dict, scatter_path,
                            [(x + 285, y - 20), (x + 551, y - 20),
                             (x + 816, y - 20), (x + 285, y + 88),
                             (x + 551, y + 88), (x + 816, y + 88),
                             (x + 285, y + 196), (x + 551, y + 196),
                             (x + 816, y + 196)] if mode == 1 else [
                                (x + 437, y + 34), (x + 707, y + 34), (x + 437, y + 142), (x + 707, y + 142),
                                (x + 437, y + 250),
                                (x + 707, y + 250), (x + 437, y + 299), (x + 707, y + 299)])
            scatter = super().get_val(tmpl_dict, scatter_path)
        print(f'scatter: {scatter}')
        return scatter

    def __individual_raid(self, index: str = ''):
        # Choose the realm
        scatter = self.__get_scatter(1)
        cur_index = 0 if not index else int(index)
        # Retreat two
        if cur_index == 8:
            # TODO
            self.retreat_two(scatter)

        super().left_click(scatter[cur_index], (1, 2))

        tmpl_raid = super().get_val(tmpl_dict, f'{self.dot_path}raid')
        pt_raid_list = super().match(tmpl_raid['path'], thresh_mul=tmpl_raid['thresh_mul'])
        print(f'pt_raid_list: {pt_raid_list}')
        # The realm has been raided
        if pt_raid_list:
            return self.__individual_raid(str(cur_index + 1))
        super().left_click(pt_raid_list[0], 2)  # Raid
        # Passes ran out
        if pt_raid_list:
            return

        time.sleep(3)
        self.__mark_ghost()
        super().conclude_battle(10, lambda: self.__individual_raid(str(cur_index + 1) if cur_index < 8 else '0'))

    def retreat_two(self, scatter):
        # Unlock
        x, y = tmpl_dict['exploration_map']['realm_raid']['buffs']
        super().left_click((x + 609, y + 333), (1, 2))
        super().left_click(scatter[-1], (1, 2))  # Choose the realm
        pt_raid_list = super().match(super().get_path(f'{self.rel_path}raid.png'),
                                     thresh_mul=0.92)
        print(f'pt_raid_list: {pt_raid_list}')
        super().left_click(pt_raid_list[0], (5, 6))  # Raid
        # Return twice
        pt_return = self.__get_pt_return()
        super().left_click(pt_return, (1, 2))
        pt_confirm = self.__get_pt_confirm()
        super().left_click(pt_confirm, (2, 3))

    def __get_pt_confirm(self):
        pt_confirm = tmpl_dict['exploration_map']['realm_raid']['individual']['confirm']
        if not pt_confirm:
            pt_confirm = tmpl_dict['exploration_map']['realm_raid']['individual']['confirm'] = super().match(
                super().get_path(f'{self.rel_path}confirm.png'))[0]
        return pt_confirm

    def __get_pt_return(self):
        pt_return = tmpl_dict['exploration_map']['realm_raid']['individual']['return']
        if not pt_return:
            pt_return = tmpl_dict['exploration_map']['realm_raid']['individual']['return'] = super().match(
                super().get_path(f'{self.rel_path}return.png'))[0]
        return pt_return


if __name__ == '__main__':
    realm_raider = RealmRaider()
    realm_raider.raid(False, False)
