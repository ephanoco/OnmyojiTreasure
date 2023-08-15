#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/7/16 1:48
# @Author  : Samuel
# @File    : tmpl_dict.py
from utils.util import Util

util = Util()
tmpl_root = 'static/templates/'
tmpl_dict = {
    'exploration': {
        'realm_raid': {
            'individual': {
                'scatter': [],
                'battle_buffs': {
                    'pt': (),
                    'path': util.get_path(f'{tmpl_root}exploration/realm_raid/battle_buffs.png'),
                    'thresh_mul': 0.9,
                },
            },
            'guild': {
                'scatter': [],
            },
            'realm_buffs': {
                'pt': (),
                'path': util.get_path(f'{tmpl_root}exploration/realm_raid/realm_buffs.png'),
                'thresh_mul': 0.97,
            },
            'raid': {
                'path': util.get_path(f'{tmpl_root}exploration/realm_raid/raid.png'),
                'thresh_mul': 0.9,
                'thresh_sgl': 0.01,
                'is_multiple': False,
                'is_with_colour': True,
            },
            'nickname': {
                'path': util.get_path(f'{tmpl_root}exploration/realm_raid/nickname.png'),
                'thresh_mul': 0.8,
            },
            'mark': {
                'path': util.get_path(f'{tmpl_root}exploration/realm_raid/mark.png'),
                'thresh_mul': 0.8,
            },
            'close': {
                'pt': (),
            },
        },
        'soul_zones': {
            'orochi': {},
            'sougenbi': {
                'challenge': {
                    'pt': (),
                    'path': util.get_path(f'{tmpl_root}exploration/soul_zones/sougenbi/challenge.png'),
                    'thresh_mul': 0.85,
                },
            },
            'fallen_sun': {},
            'sea_of_eternity': {},
            'sougenbi_btn': {
                'pt': (),
                'path': util.get_path(f'{tmpl_root}exploration/soul_zones/sougenbi_btn.png'),
            },
        },
        'common': {
            'victory': {
                'path': util.get_path(f'{tmpl_root}exploration/common/victory.png'),
                'thresh_mul': 0.96,
            },
            'defeat': {
                'path': util.get_path(f'{tmpl_root}exploration/common/defeat.png'),
            },
        },
        'realm_raid_btn': {
            'pt': (),
            'path': util.get_path(f'{tmpl_root}exploration/realm_raid_btn.png'),
            'thresh_mul': 0.98,
        },
    },
    'town': {
        'demon_parade': {
            'invite': {
                'pt': (),
                'path': util.get_path(f'{tmpl_root}town/demon_parade/invite.png'),
            },
            'friend_list_scatter': [],
            'friends': {
                'path': util.get_path(f'{tmpl_root}town/demon_parade/friends.png'),
            },
            'enter': {
                'pt': (),
                'path': util.get_path(f'{tmpl_root}town/demon_parade/enter.png'),
            },
            'start': {
                'pt': (),
                'path': util.get_path(f'{tmpl_root}town/demon_parade/start.png'),
            },
            'ghosts_scatter': [],
        }
    },
    'wanted_quests': {
        'invitation': {
            'path': util.get_path(f'{tmpl_root}wanted_quests/invitation.png'),
        },
        'gold': {
            'path': util.get_path(f'{tmpl_root}wanted_quests/gold.png'),
        },
        'accept': (),
        'reject': (),
        'shard': {
            'path': util.get_path(f'{tmpl_root}wanted_quests/shard.png'),
        },
    }
}
