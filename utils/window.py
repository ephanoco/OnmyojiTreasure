#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 17:02
# @Author  : Samuel
# @File    : window.py
from ctypes.wintypes import HWND

import win32api
import win32gui

from utils.util import Util


class Window(Util):
    def __init__(self):
        # self.hwnd: HWND = win32gui.FindWindow(None, '阴阳师 - MuMu模拟器')
        self.hwnd: HWND = self.get_hwnd()

    def get_hwnd(self):
        # hwnd_list = self.__get_hwnd_list()
        # for hwnd in hwnd_list:
        #     wnd_text = self.__get_wnd_text(hwnd)
        #     if 'MuMu模拟器' in wnd_text:
        #         return hwnd
        print('Please place the cursor inside the window to get a handle.')
        super().countdown(10)
        pt = win32api.GetCursorPos()
        hwnd = win32gui.WindowFromPoint(pt)
        print(f'hwnd: {hwnd}')
        wnd_text = self.__get_wnd_text(hwnd)
        print(f'wnd_text: {wnd_text}')
        return hwnd

    @staticmethod
    def __get_wnd_text(hwnd):
        return win32gui.GetWindowText(hwnd)

    @staticmethod
    def __get_hwnd_list():
        hwnd_list = []
        win32gui.EnumWindows(lambda hwnd, param: param.append(hwnd), hwnd_list)
        return hwnd_list


if __name__ == '__main__':
    window = Window()
