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

    def match(self, tmpl_path, capture=True, is_multiple=True, thresh_mul=0.99, thresh_sgl=0.03, is_with_colour=False):
        if capture:
            super().capture()
        img_rgb = cv.imread(super().get_path('static/screenshot.png'))
        tmpl_rgb = cv.imread(tmpl_path)
        return self.match_template(img_rgb, tmpl_rgb, is_multiple, thresh_mul, thresh_sgl, is_with_colour)

    def match_template(self, img_rgb, tmpl_rgb, is_multiple, thresh_mul, thresh_sgl, is_with_colour):
        res = self.__get_res(is_with_colour, img_rgb, is_multiple, tmpl_rgb)
        w, h = tmpl_rgb.shape[1::-1]  # = tmpl_gray.shape[::-1]
        if is_multiple:
            loc = np.where(res >= thresh_mul)
            pt_list = []
            for pt in zip(*loc[::-1]):
                cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), 255, 2)
                pt = self.__get_converted_pt((pt[0] + w / 2, pt[1] + h / 2))
                pt_list.append(pt)
            cv.imwrite('res.png', img_rgb)
            return pt_list
        else:
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            top, left = top_left = min_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv.rectangle(img_rgb, top_left, bottom_right, 255, 2)
            cv.imwrite('res.png', img_rgb)
            pt = self.__get_converted_pt((top + w / 2, left + h / 2))
            return pt if min_val <= thresh_sgl else ()

    @staticmethod
    def __get_res(is_with_colour, img_rgb, is_multiple, tmpl_rgb):
        meth = cv.TM_SQDIFF_NORMED if not is_multiple else cv.TM_CCOEFF_NORMED
        if not is_with_colour:
            img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
            tmpl_gray = cv.cvtColor(tmpl_rgb, cv.COLOR_BGR2GRAY)
            res = cv.matchTemplate(img_gray, tmpl_gray, meth)
        else:
            b_img, g_img, r_img = cv.split(img_rgb)
            b_tmpl, g_tmpl, r_tmpl = cv.split(tmpl_rgb)
            res_b = cv.matchTemplate(b_img, b_tmpl, meth)
            res_g = cv.matchTemplate(g_img, g_tmpl, meth)
            res_r = cv.matchTemplate(r_img, r_tmpl, meth)
            cv.normalize(res_b, res_b, 0, 1, cv.NORM_MINMAX, -1)
            cv.normalize(res_g, res_g, 0, 1, cv.NORM_MINMAX, -1)
            cv.normalize(res_r, res_r, 0, 1, cv.NORM_MINMAX, -1)
            res = (res_b + res_g + res_r) / 3.0
        return res

    def __get_converted_pt(self, pt):
        x, y = pt
        return win32gui.ClientToScreen(self.hwnd, (int(x), int(y)))


if __name__ == '__main__':
    matcher = Matcher()
    util = Util()
    pt_list = matcher.match(util.get_path('static/templates/explore_map/realm_raid/raid.png'), False, False,
                            thresh_sgl=0.02,
                            is_with_colour=True)
    print(f'pt_list: {pt_list}')
