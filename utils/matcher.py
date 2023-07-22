#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 17:01
# @Author  : Samuel
# @File    : matcher.py
import cv2 as cv
import numpy as np
import win32gui

from utils.capturer import Capturer
from utils.util import Util


class Matcher(Capturer, Util):
    def __init__(self):
        super().__init__()

    def match(self, tmpl_path, capture=True, is_multiple=True, threshold=0.99):
        if capture:
            super().capture()
        img_rgb = cv.imread(super().get_path('static/screenshot.png'))
        template = cv.imread(tmpl_path, cv.IMREAD_GRAYSCALE)
        return self.match_template(img_rgb, template, is_multiple, threshold)

    def match_template(self, img_rgb, template, is_multiple, threshold):
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]
        if not is_multiple:
            res = cv.matchTemplate(img_gray, template, cv.TM_SQDIFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            top, left = top_left = min_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv.rectangle(img_rgb, top_left, bottom_right, 255, 2)
            cv.imwrite('res.png', img_rgb)
            pt = self.__get_converted_pt((top + w / 2, left + h / 2))
            if min_val <= 0.03:  # XXX
                return pt
            else:
                return ()
        else:
            res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
            loc = np.where(res >= threshold)
            pt_list = []
            for pt in zip(*loc[::-1]):
                cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), 255, 2)
                pt = self.__get_converted_pt((pt[0] + w / 2, pt[1] + h / 2))
                pt_list.append(pt)
            cv.imwrite('res.png', img_rgb)
            return pt_list

    def __get_converted_pt(self, pt):
        x, y = pt
        return win32gui.ClientToScreen(self.hwnd, (int(x), int(y)))


if __name__ == '__main__':
    matcher = Matcher()
    util = Util()
    pt_list = matcher.match(util.get_path('static/templates/explore_map/realm_raid/realm_raid.png'), False)
    print(f'pt_list: {pt_list}')
