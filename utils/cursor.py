#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 17:01
# @Author  : Samuel
# @File    : cursor.py
import random
import time

import win32api
import win32con
import win32gui

from utils.window import Window


class Cursor(Window):
    @staticmethod
    def __set_cursor_pos(pt):
        """
        Move the cursor.
        :param pt:
        :return:
        """
        cx, cy = pt
        win32api.SetCursorPos((cx, cy))

    @staticmethod
    def __get_offset_pt(pt):
        cx, cy = pt
        offset_y = offset_x = random.randint(-5, 5)  # random.randint(0, 10)
        return cx + offset_x, cy + offset_y

    def left_click(self, pt, delay: int | float | tuple = None):
        """

        :param pt:
        :param delay:delay after click
        :return:
        """
        offset_pt = self.__get_offset_pt(pt)
        # Frontstage
        # self.__set_cursor_pos(offset_pt)
        # time.sleep(0.1)
        # cx, cy = offset_pt
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, cx, cy)
        # Backstage
        cx, cy = win32gui.ScreenToClient(self.hwnd, offset_pt)
        lParam = win32api.MAKELONG(cx, cy)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
        win32api.SendMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)
        if isinstance(delay, int | float):
            time.sleep(delay)
        elif isinstance(delay, tuple):
            start, stop = delay
            random_delay = random.uniform(start, stop)
            time.sleep(random_delay)


if __name__ == '__main__':
    cursor = Cursor()
    cursor.left_click((1046, 327))
