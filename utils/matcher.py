#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 17:01
# @Author  : Samuel
# @File    : matcher.py
import cv2 as cv
import numpy as np
import win32gui

from utils.capturer import Capturer
from utils.cursor import Cursor
from utils.pt_dict import pt_dict
from utils.util import Util


class Matcher(Capturer, Cursor):
    def __init__(self):
        super().__init__()

    def match(self, tmpl_path, capture=True, is_multiple=True, thresh_mul=0.99, thresh_sgl=0.03, is_with_colour=False,
              classification=1):
        kwargs = locals()
        if capture:
            super().capture()
        img_rgb = cv.imread(super().get_path('static/screenshot.png'))
        self.__mission_invitation_handler(img_rgb, kwargs)
        tmpl_rgb = cv.imread(tmpl_path)
        return self.match_template(img_rgb, tmpl_rgb, is_multiple, thresh_mul, thresh_sgl,
                                   is_with_colour) if classification == 1 else self.match_features(img_rgb, tmpl_rgb)

    def __mission_invitation_handler(self, img_rgb, kwargs):
        rel_path = 'static/templates/wanted_quests/'
        pt_inv_list = self.match_template(img_rgb, cv.imread(super().get_path(f'{rel_path}invitation.png')))
        if pt_inv_list:
            pt_gold_list = self.match_template(img_rgb, cv.imread(super().get_path(f'{rel_path}gold.png')))
            pt_accept, pt_reject = self.__get_pt_accept_reject(pt_inv_list[0])
            if not pt_gold_list:
                super().left_click(pt_accept, (1, 2))
            else:
                pt_shard_list = self.match_template(img_rgb, cv.imread(super().get_path(f'{rel_path}shard.png')))
                super().left_click(pt_accept if not pt_shard_list else pt_reject, (1, 2))
            return self.match(**kwargs)

    def __get_pt_accept_reject(self, pt_inv):
        x, y = pt_inv
        pt_accept = pt_dict['wanted_quests']['accept']
        if not pt_accept:
            pt_accept = pt_dict['wanted_quests']['accept'] = (x + 255, y + 195)
        pt_reject = pt_dict['wanted_quests']['reject']
        if not pt_reject:
            pt_reject = pt_dict['wanted_quests']['reject'] = (x + 254, y + 276)
        return [pt_accept, pt_reject]

    def match_template(self, img_rgb, tmpl_rgb, is_multiple=True, thresh_mul=0.99, thresh_sgl=0.03,
                       is_with_colour=False):
        res = self.__get_res(is_with_colour, img_rgb, is_multiple, tmpl_rgb)
        w, h = tmpl_rgb.shape[1::-1]  # = tmpl_gray.shape[::-1]
        if is_multiple:
            loc = np.where(res >= thresh_mul)
            pt_list = []
            for pt in zip(*loc[::-1]):
                # cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), 255, 2)
                pt = self.__get_converted_pt((pt[0] + w / 2, pt[1] + h / 2))
                pt_list.append(pt)
            # cv.imwrite('res.png', img_rgb)
            return pt_list
        else:
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            top, left = top_left = min_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            # cv.rectangle(img_rgb, top_left, bottom_right, 255, 2)
            # cv.imwrite('res.png', img_rgb)
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

    def match_features(self, img_rgb, tmpl_rgb):
        # Find the key points and descriptors with SIFT
        query_img = cv.cvtColor(tmpl_rgb, cv.COLOR_BGR2GRAY)
        query_kp, query_des = self.__get_kp_des(query_img)
        train_img = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        train_kp, train_des = self.__get_kp_des(train_img)
        matches = self.__flann_match(query_des, train_des)  # FLANN parameters
        # matches_mask = [[0, 0] for i in range(len(matches))]  # Need to draw only good matches, so create a mask
        # draw_params = dict(matchColor=(0, 255, 0),
        #                    singlePointColor=(255, 0, 0),
        #                    matchesMask=matches_mask,
        #                    flags=cv.DrawMatchesFlags_DEFAULT)
        # ratio test as per Lowe's paper
        train_kp_list = []
        for i, (m, n) in enumerate(matches):
            if m.distance < 0.7 * n.distance:
                # matches_mask[i] = [1, 0]
                train_kp_list.append([train_kp[matches[i][0].trainIdx].pt[0], train_kp[matches[i][0].trainIdx].pt[1]])
        train_kp = self.__get_train_kp(train_kp_list) if len(train_kp_list) else ()

        # output_img = cv.drawMatchesKnn(query_img, query_kp, train_img, train_kp, matches, None, **draw_params)
        # cv.imwrite('res.png', output_img)
        return train_kp

    def __get_train_kp(self, train_kp_list):
        x, y = (0, 0)
        for i in range(len(train_kp_list)):
            x += train_kp_list[i][0]
            y += train_kp_list[i][1]
        return self.__get_converted_pt((x / len(train_kp_list), y / len(train_kp_list)))

    @staticmethod
    def __flann_match(query_des, train_des):
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(query_des, train_des, k=2)
        return matches

    @staticmethod
    def __get_kp_des(img):
        # noinspection PyUnresolvedReferences
        sift = cv.SIFT_create()
        kp, des = sift.detectAndCompute(img, None)
        return kp, des


if __name__ == '__main__':
    matcher = Matcher()
    util = Util()
    train_kp = matcher.match(util.get_path('static/templates/town/demon_parade/ghosts/hitotsume_kozou.png'), False,
                             classification=2)
    print(f'train_kp: {train_kp}')
