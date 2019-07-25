# -*- coding: utf-8 -*-
#
# @author: Toso
# @created: Sun Oct 07 2018 11:06:27 GMT+0800 (中国标准时间)
# @comment: ______________
#


def GetSeatType(seat_type):
    if seat_type == '商务座特等座':
        seat_type_index = 1
        seat_type_value = '9'
    elif seat_type == '一等座':
        seat_type_index = 2
        seat_type_value = 'M'
    elif seat_type == '二等座':
        seat_type_index = 3
        seat_type_value = 'O'
    elif seat_type == '高级软卧':
        seat_type_index = 4
        seat_type_value = '6'
    elif seat_type == '软卧':
        seat_type_index = 5
        seat_type_value = '4'
    elif seat_type == '动卧':
        seat_type_index = 6
        seat_type_value = 'F'
    elif seat_type == '硬卧':
        seat_type_index = 7
        seat_type_value = '3'
    elif seat_type == '软座':
        seat_type_index = 8
        seat_type_value = '2'
    elif seat_type == '硬座':
        seat_type_index = 9
        seat_type_value = '1'
    elif seat_type == '无座':
        seat_type_index = 10
        seat_type_value = '1'
    elif seat_type == '其他':
        seat_type_index = 11
        seat_type_value = '1'
    else:
        seat_type_index = 7
        seat_type_value = '3'
    
    return seat_type_value


