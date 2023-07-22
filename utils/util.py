#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 17:02
# @Author  : Samuel
# @File    : util.py
import ctypes
import os.path


class Util:
    @staticmethod
    def get_path(path):
        cur_path = os.path.dirname(__file__)
        base_dir = os.path.dirname(cur_path)
        return os.path.join(base_dir, os.path.normcase(path))

    @staticmethod
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def get_converted_pt_list(self, pt_list):
        return sorted(pt_list, key=lambda x: x[1])


if __name__ == '__main__':
    util = Util()
    util.get_converted_pt_list([(735, 251), (977, 248), (707, 356), (945, 356), (675, 464), (945, 464)])
