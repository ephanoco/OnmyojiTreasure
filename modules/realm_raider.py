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
        self.rel_path = 'static/templates/explore_map/realm_raid/'
        self.guild_defeated_count = 0

    def raid(self):
        is_individual = len(super().match(
            super().get_path(f'{self.rel_path}individual_active.png'), threshold=0.98
        )) != 0
        if is_individual:
            self.__individual_raid()
        else:
            self.__guild_raid()

    def __guild_raid(self, index: str = ''):
        # Choose the realm
        scatter = self.__get_guild_scatter()
        cur_index = self.guild_defeated_count
        if index:
            cur_index = int(index)
        super().left_click(scatter[cur_index], (1, 2))

        pt_raid_list = super().match(
            super().get_path(f'{self.rel_path}raid.png'), threshold=0.92)
        print(f'pt_raid_list: {pt_raid_list}')
        # Successful penetration
        if not pt_raid_list:
            return

        super().left_click(pt_raid_list[0], 2)  # Raid
        # The realm has been raided
        pt_raid_list = super().match(super().get_path(f'{self.rel_path}raid.png'), threshold=0.92)
        if pt_raid_list:
            super().left_click(scatter[cur_index + 1], (1, 2))
            return self.__guild_raid(str(cur_index + 1))

        time.sleep(2)
        self.__mark_ghost()
        is_first_loop = True
        while True:
            if is_first_loop:
                time.sleep(10)
                is_first_loop = False
            else:
                time.sleep(1)
            super().capture()
            pt_victory_list = super().match(super().get_path(f'{self.rel_path}victory.png'), False, threshold=0.96)
            if pt_victory_list:
                time.sleep(1)
                super().left_click(pt_victory_list[0], (4, 5))
                self.__guild_raid()
                break
            pt_defeat_list = super().match(super().get_path(f'{self.rel_path}defeat.png'), False)
            if pt_defeat_list:
                super().left_click(pt_defeat_list[0], (4, 5))
                self.guild_defeated_count += 1
                if self.guild_defeated_count <= len(scatter):
                    self.__guild_raid()
                break

    def __mark_ghost(self, pt=(), times=0):
        if times == 5:
            return
        if not pt:
            pt_ghost = self.__get_pt_ghost()
        else:
            pt_ghost = pt
        super().left_click(pt_ghost, 0.4, True)
        super().capture()
        is_marked_light = len(super().match(super().get_path(f'{self.rel_path}mark.png'), False, threshold=0.9)) != 0
        print(f'is_marked[light]: {is_marked_light}')
        if is_marked_light:
            is_marked = True
        else:
            is_marked = (len(
                super().match(super().get_path(f'{self.rel_path}mark_dark.png'), False)) != 0)
            print(f'is_marked[dark]: {is_marked}')
        if not is_marked:
            self.__mark_ghost(pt_ghost, times=times + 1)

    def __get_pt_ghost(self, times=0):
        if times == 9:
            return
        super().capture()
        pt_ghost_light_list = super().match(
            super().get_path(f'{self.rel_path}ghost.png'), False, threshold=0.84)
        print(f'pt_ghost_list[light]: {pt_ghost_light_list}')
        if pt_ghost_light_list:
            return pt_ghost_light_list[0]
        pt_ghost_dark_list = super().match(
            super().get_path(f'{self.rel_path}ghost_dark.png'), False, threshold=0.82)
        print(f'pt_ghost_list[dark]: {pt_ghost_dark_list}')
        if pt_ghost_dark_list:
            return pt_ghost_dark_list[0]
        time.sleep(0.2)  # XXX
        return self.__get_pt_ghost(times + 1)

    def __get_guild_scatter(self):
        scatter = pt_dict['explore_map']['realm_raid']['guild']['scatter']
        if not scatter:
            x, y = super().match(super().get_path(f'{self.rel_path}realm_raid.png'))[0]
            scatter = pt_dict['explore_map']['realm_raid'][
                'guild']['scatter'] = [(x + 25, y + 104), (x + 295, y + 104), (x + 25, y + 212), (x + 295, y + 212),
                                       (x + 25, y + 320), (x + 295, y + 320)]
        print(f'scatter: {scatter}')
        return scatter

    @staticmethod
    def __individual_raid():
        pass


if __name__ == '__main__':
    realm_raider = RealmRaider()
    realm_raider.raid()
