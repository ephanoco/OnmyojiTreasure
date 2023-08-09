#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 17:02
# @Author  : Samuel
# @File    : util.py
import os.path
import sys
import time


class Util:
    @staticmethod
    def get_path(path):
        """
        Get the absolute path of the file.
        :param path:File relative path
        :return:File absolute path
        """
        cur_path = os.path.dirname(__file__)
        base_dir = os.path.dirname(cur_path)
        return os.path.join(base_dir, os.path.normcase(path))

    @staticmethod
    def get_converted_pt_list(pt_list):
        return sorted(pt_list, key=lambda x: x[1])

    @staticmethod
    def query_mode(modes):
        # Select the mode
        for c, desc in modes.items():
            print(f"{c}. {desc}")
        choice = input("Select your mode: ")
        while choice not in modes:
            choice = input(f"Choose one of: {', '.join(modes)}: ")
        print(f"Role: {modes[choice]}")
        return choice

    @staticmethod
    def query_yes_no(question, default="yes"):
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

    @staticmethod
    def countdown(t):
        """

        :param t:Time in seconds
        :return:
        """
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            time.sleep(1)
            t -= 1


if __name__ == '__main__':
    util = Util()
    util.countdown(10)
