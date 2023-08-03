#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/22 17:16
# @Author  : Samuel
# @File    : beans_thrower.py
import time

from utils.cursor import Cursor
from utils.matcher import Matcher
from utils.tmpl_dict import tmpl_dict


class BeansThrower(Matcher, Cursor):
    def __init__(self):
        super().__init__()
        self.dict_demon_parade = tmpl_dict['town']['demon_parade']

    def throw_beans(self):
        self.__invite_friends()  # Choose the friend
        # Enter the ghost selection screen
        pt_enter = self.dict_demon_parade['enter']['pt']
        if not pt_enter:
            pt_enter = self.dict_demon_parade['enter']['pt'] = super().match(self.dict_demon_parade['enter']['path'])[0]
        super().left_click(pt_enter, (4, 5))
        super().capture(True, 'static/TODO/town/demon_parade/ghost_selection_screen/')  # HACK
        pt_start = self.dict_demon_parade['start']['pt']
        if not pt_start:
            pt_start = self.dict_demon_parade['start']['pt'] = super().match(self.dict_demon_parade['start']['path'])[0]
        self.__choose_ghost(pt_start)  # Choose the ghost
        super().left_click(pt_start, (4, 5))
        # TODO

        while True:
            time.sleep(1)
            super().capture(True, 'static/TODO/town/demon_parade/ghosts/')  # HACK

    def __choose_ghost(self, pt_start):
        ghosts_scatter = self.__get_ghosts_scatter(pt_start)
        super().left_click(ghosts_scatter[2], (1, 2))  # The right ghost is selected by default

    def __get_ghosts_scatter(self, pt_start):
        scatter = self.dict_demon_parade['ghosts_scatter']
        if not scatter:
            x, y = pt_start
            scatter = self.dict_demon_parade['ghosts_scatter'] = [(x - 689, y - 92), (x - 398, y - 124),
                                                                  (x - 114, y - 103)]
        print(f'ghosts_scatter: {scatter}')
        return scatter

    def __invite_friends(self, index: str = ''):
        # Clicking on the '+' button
        pt_invite = self.dict_demon_parade['invite']['pt']
        if not pt_invite:
            pt_invite = self.dict_demon_parade['invite']['pt'] = \
                super().match(self.dict_demon_parade['invite']['path'])[0]
        super().left_click(pt_invite, (1, 2))
        # Invite someone from friend list
        friend_list_scatter = self.__get_friend_list_scatter()
        cur_index = 0 if not index else int(index)
        super().left_click(friend_list_scatter[cur_index], (1, 2))

    def __get_friend_list_scatter(self):
        scatter = self.dict_demon_parade['friend_list_scatter']
        if not scatter:
            x, y = super().match(self.dict_demon_parade['friends']['path'])[0]
            scatter = self.dict_demon_parade['friend_list_scatter'] = [(x + 100, y + 64), (x + 316, y + 64),
                                                                       (x + 100, y + 131), (x + 316, y + 131),
                                                                       (x + 100, y + 199), (x + 316, y + 199),
                                                                       (x + 100, y + 266), (x + 316, y + 266)]
        print(f'friend_list_scatter: {scatter}')
        return scatter


if __name__ == '__main__':
    beans_thrower = BeansThrower()
    beans_thrower.throw_beans()
