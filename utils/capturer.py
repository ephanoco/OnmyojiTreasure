#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 17:01
# @Author  : Samuel
# @File    : capturer.py
import sys
import time

import win32con
import win32gui
import win32ui

from utils.util import Util
from utils.window import Window


class Capturer(Window, Util):
    def __init__(self):
        super().__init__()

    def capture(self, is_with_timestamp=False, storage_path=''):
        """

        :param is_with_timestamp: Filename contains timestamp.
        :param storage_path:
        :return:
        """
        if not self.hwnd:
            sys.exit()
        bitmap = win32ui.CreateBitmap()
        wnd_dc = win32gui.GetWindowDC(self.hwnd)
        hdc = win32ui.CreateDCFromHandle(wnd_dc)

        # Get the bitmap width and height
        (left, top, right, bottom) = win32gui.GetWindowRect(self.hwnd)
        cx = right - left
        cy = bottom - top

        bitmap.CreateCompatibleBitmap(hdc, cx, cy)
        mem_dc = hdc.CreateCompatibleDC()
        mem_dc.SelectObject(bitmap)
        mem_dc.BitBlt((0, 0), (cx, cy), hdc, (0, 0), win32con.SRCCOPY)

        # Save the screenshot
        bitmap.SaveBitmapFile(mem_dc,
                              super().get_path('static/screenshot.png') if not is_with_timestamp else super().get_path(
                                  f'{storage_path}screenshot_{time.time()}.png'))
        # Release memory
        win32gui.DeleteObject(bitmap.GetHandle())
        hdc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wnd_dc)
        mem_dc.DeleteDC()


if __name__ == '__main__':
    capturer = Capturer()
    capturer.capture()
