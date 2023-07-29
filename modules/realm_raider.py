#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 17:00
# @Author  : Samuel
# @File    : realm_raider.py
import time

from utils.cursor import Cursor
from utils.matcher import Matcher
from utils.pt_dict import pt_dict


class RealmRaider(Matcher, Cursor):
    def __init__(self):
        super().__init__()
        self.rel_path = 'static/templates/exploration_map/realm_raid/'
        self.guild_defeated_count = 0

    def raid(self, is_individual, is_cooldown):
        # is_individual = len(super().match(
        #     super().get_path(f'{self.rel_path}individual_active.png'), thresh_mul=0.98
        # )) != 0
        self.__individual_raid() if is_individual else self.__guild_raid(is_cooldown)

    def __guild_raid(self, is_cooldown, index: str = ''):
        # Choose the realm
        scatter = self.__get_guild_scatter()
        cur_index = self.guild_defeated_count if not index else int(index)
        super().left_click(scatter[cur_index], (1, 2))

        pt_raid_list = super().match(super().get_path(f'{self.rel_path}raid.png'),
                                     thresh_mul=0.92) if not is_cooldown else [
            super().match(super().get_path(f'{self.rel_path}raid.png'), is_multiple=False, thresh_sgl=0.01,
                          is_with_colour=True)]
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
        pt_raid_list = super().match(super().get_path(f'{self.rel_path}raid.png'), thresh_mul=0.92)
        if pt_raid_list:
            super().left_click(scatter[cur_index + 1], (1, 2))
            return self.__guild_raid(is_cooldown, str(cur_index + 1))

        time.sleep(3)
        self.__mark_ghost()
        is_first_loop = True
        while True:
            if is_first_loop:
                time.sleep(10)
                is_first_loop = False
            else:
                time.sleep(1)
            super().capture()
            pt_victory_list = super().match(super().get_path(f'{self.rel_path}victory.png'), False, thresh_mul=0.96)
            if pt_victory_list:
                time.sleep(1)
                super().left_click(pt_victory_list[0], (4, 5))
                self.__guild_raid(is_cooldown)
                break
            pt_defeat_list = super().match(super().get_path(f'{self.rel_path}defeat.png'), False)
            if pt_defeat_list:
                super().left_click(pt_defeat_list[0], (4, 5))
                self.guild_defeated_count += 1
                if self.guild_defeated_count <= len(scatter):
                    self.__guild_raid(is_cooldown)
                break

    def __mark_ghost(self, pt=(), times=0):
        if times == 10:
            return
        pt_ghost = self.__get_pt_ghost() if not pt else pt
        super().left_click(pt_ghost, 0.4)
        super().capture()
        is_marked_light = len(super().match(super().get_path(f'{self.rel_path}mark.png'), False, thresh_mul=0.8)) != 0
        print(f'is_marked[light]: {is_marked_light}')
        if is_marked_light:
            is_marked = True
        else:
            is_marked = (len(
                super().match(super().get_path(f'{self.rel_path}mark_dark.png'), False, thresh_mul=0.8)) != 0)
            print(f'is_marked[dark]: {is_marked}')
        if not is_marked:
            self.__mark_ghost(pt_ghost, times=times + 1)

    def __get_pt_ghost(self):
        x, y = self.__get_pt_nickname()
        return x + 6, y + 74

    def __get_pt_nickname(self):
        super().capture()
        pt_nickname_light_list = super().match(
            super().get_path(f'{self.rel_path}nickname.png'), False, thresh_mul=0.8)
        print(f'pt_nickname_list[light]: {pt_nickname_light_list}')
        if pt_nickname_light_list:
            return pt_nickname_light_list[0]
        pt_nickname_dark_list = super().match(
            super().get_path(f'{self.rel_path}nickname_dark.png'), False, thresh_mul=0.8)
        print(f'pt_nickname_list[dark]: {pt_nickname_dark_list}')
        if pt_nickname_dark_list:
            return pt_nickname_dark_list[0]
        time.sleep(0.2)  # XXX
        return self.__get_pt_nickname()

    def __get_guild_scatter(self):
        scatter = pt_dict['exploration_map']['realm_raid']['guild']['scatter']
        if not scatter:
            pt_buffs = pt_dict['exploration_map']['realm_raid']['guild']['buffs']
            if not pt_buffs:
                pt_buffs = pt_dict['exploration_map']['realm_raid']['guild']['buffs'] = \
                    super().match(super().get_path(f'{self.rel_path}buffs.png'), thresh_mul=0.97)[0]
            x, y = pt_buffs
            scatter = pt_dict['exploration_map']['realm_raid'][
                'guild']['scatter'] = [(x + 437, y + 34), (x + 707, y + 34), (x + 437, y + 142), (x + 707, y + 142),
                                       (x + 437, y + 250), (x + 707, y + 250)]
        print(f'scatter: {scatter}')
        return scatter

    @staticmethod
    def __individual_raid():
        pass


if __name__ == '__main__':
    realm_raider = RealmRaider()
    realm_raider.raid(False, False)
