#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/22 17:16
# @Author  : Samuel
# @File    : beans_thrower.py
from utils.cursor import Cursor
from utils.matcher import Matcher
from utils.pt_dict import pt_dict


class BeansThrower(Matcher, Cursor):
    def __init__(self):
        super().__init__()
        self.rel_path = 'static/templates/town/demon_parade/'

    def throw_beans(self):
        self.__invite_friends()

    def __invite_friends(self):
        pt_invite = pt_dict['town']['demon_parade']['invite']
        if not pt_invite:
            pt_invite = pt_dict['town']['demon_parade']['invite'] = super().match(
                super().get_path(f'{self.rel_path}invite.png'))[0]
        super().left_click(pt_invite, (1, 2))


if __name__ == '__main__':
    beans_thrower = BeansThrower()
    beans_thrower.throw_beans()
