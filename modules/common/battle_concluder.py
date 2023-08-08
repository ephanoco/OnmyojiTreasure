#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/2 22:13
# @Author  : Samuel
# @File    : battle_concluder.py
import time

from utils.matcher import Matcher
from utils.tmpl_dict import tmpl_dict


class BattleConcluder(Matcher):
    def __init__(self):
        super().__init__()
        self.dict_common = tmpl_dict['exploration']['common']

    def conclude_battle(self, first_loop_delay, vic_cb, is_loop_def=True, def_cb=None):
        """

        :param first_loop_delay:Minimum battle duration
        :param vic_cb:
        :param is_loop_def:Continue after defeat.
        :param def_cb:
        :return:
        """
        is_first_loop = True
        while True:
            if is_first_loop:
                time.sleep(first_loop_delay)
                is_first_loop = False
            else:
                time.sleep(1)
            super().capture()
            tmpl_victory = self.dict_common['victory']
            pt_victory_list = super().match(tmpl_victory['path'], False,
                                            thresh_mul=tmpl_victory['thresh_mul'])
            if pt_victory_list:
                time.sleep(1)
                super().left_click(pt_victory_list[0], (4, 5))
                vic_cb()
                break
            pt_defeat_list = super().match(self.dict_common['defeat']['path'], False)
            if pt_defeat_list:
                if is_loop_def:
                    super().left_click(pt_defeat_list[0], (4, 5))
                if def_cb:
                    def_cb()
                break
