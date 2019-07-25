# -*- coding: utf-8 -*-
#
# @author: Toso
# @created: Mon Oct 01 2018 12:22:36 GMT+0800 (中国标准时间)
# @comment: ______________
#

import re
import urllib2
from base64 import encode
import config

dict = {}

def GetStation():
    #####获取站点信息#######
    station_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9069'
    response = urllib2.urlopen(urllib2.Request(
            station_url, headers=config.headers))
    jstxt = response.read().split('\'')[1]
    station = jstxt.split('@')

    for item in station:
        if item != '':
            v = item.split('|')
            dict[v[1]] = v[2]
    print('GetStation Suc...')

def GetStationDict(s):
    return dict[s]

def GetStationName(s):
    for key, val in dict.items():
        if val == s:
            return key

#GetStation()
#print GetStationDict('武汉')
#print GetStationName('GZQ')