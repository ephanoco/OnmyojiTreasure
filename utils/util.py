#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 17:02
# @Author  : Samuel
# @File    : util.py
import ctypes
import os.path
import sys


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

    def query_yes_no(self, question, default="yes"):
        """Ask a yes/no question via raw_input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
                It must be "yes" (the default), "no" or None (meaning
                an answer is required of the user).

        The "answer" return value is True for "yes" or False for "no".
        """
        valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if default is not None and choice == "":
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


if __name__ == '__main__':
    util = Util()
    util.get_converted_pt_list([(735, 251), (977, 248), (707, 356), (945, 356), (675, 464), (945, 464)])
