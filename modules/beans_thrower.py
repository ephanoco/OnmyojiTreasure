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
        pt_start = self.dict_demon_parade['start']['pt']
        if not pt_start:
            pt_start = self.dict_demon_parade['start']['pt'] = super().match(self.dict_demon_parade['start']['path'])[0]
        self.__choose_ghost(pt_start)  # Choose the ghost
        super().left_click(pt_start, (4, 5))
        # TODO
        while True:
            time.sleep(1)
            super().capture(True, 'static/temp/town/demon_parade/ghosts/')  # HACK

    def __choose_ghost(self, pt_start):
        ghosts_scatter = self.__get_ghosts_scatter(pt_start)
        super().left_click(ghosts_scatter[2], (1, 2))  # The right ghost is selected by default

    def __get_ghosts_scatter(self, pt_start):
        scatter = self.dict_demon_parade['ghosts_scatter']
        if not scatter:
            cx, cy = pt_start
            scatter = self.dict_demon_parade['ghosts_scatter'] = [(cx - 689, cy - 92), (cx - 398, cy - 124),
                                                                  (cx - 114, cy - 103)]
        print(f'scatter[ghosts]: {scatter}')
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
            cx, cy = super().match(self.dict_demon_parade['friends']['path'])[0]
            scatter = self.dict_demon_parade['friend_list_scatter'] = [(cx + 100, cy + 64), (cx + 316, cy + 64),
                                                                       (cx + 100, cy + 131), (cx + 316, cy + 131),
                                                                       (cx + 100, cy + 199), (cx + 316, cy + 199),
                                                                       (cx + 100, cy + 266), (cx + 316, cy + 266)]
        print(f'scatter[friend_list]: {scatter}')
        return scatter


if __name__ == '__main__':
    beans_thrower = BeansThrower()
    beans_thrower.throw_beans()
