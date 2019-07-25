# -*- coding: utf-8 -*-
#
# @author: Toso
# @created: Sun Sep 30 2018 10:25:49 GMT+0800 (中国标准时间)
# @comment: ______________
#

import time
import datetime

from PIL import Image
from bs4 import BeautifulSoup
from prettytable import PrettyTable

import config
import cookielib
import json
import re
import seat
import ssl
import station
import urllib2
from codecs import decode, encode
from io import BytesIO
from logging import exception
from string import rstrip
from urllib import unquote, urlencode
import random
import Email


ssl._create_default_https_context = ssl._create_unverified_context


def WebCookie():
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)


"""
    12306 登录
"""


def login():
    WebCookie()
    # 打开登陆页面
    response = urllib2.urlopen(urllib2.Request(
        config.init_url, headers=config.headers))
    if response.getcode() == 200:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        print soup.find(id="login_user").text.strip().encode('gbk')

    # 发送验证码
    while not captcha():
        time.sleep(1)

    # 发送登录信息
    response = urllib2.urlopen(urllib2.Request(
        config.login_url, headers=config.headers), data=urlencode(config.logininfo))
    if response.getcode() == 200:
        result = json.loads(response.read())
        print(result.get('result_message').encode('gbk'))
        if result.get('result_code') != 0:
            return False

    response = urllib2.urlopen(urllib2.Request(
        config.uamtk_url, headers=config.headers), data=urlencode({"appid": "otn"}))
    if response.getcode() == 200:
        result = json.loads(response.read())
        print("uamtk:" + result.get("result_message").encode('gbk'))
        newapptk = result.get("newapptk")

    response = urllib2.urlopen(urllib2.Request(
        config.auth_url, headers=config.headers), data=urlencode({"tk": newapptk}))
    if response.getcode() == 200:
        result = json.loads(response.read())
        print("auth:" + result.get("result_message").encode('gbk'))
        print("username:" + result.get("username").encode('gbk'))

    response = urllib2.urlopen(urllib2.Request(
        config.initmy12306_url, headers=config.headers))
    if response.getcode() == 200:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        name = soup.find(id="login_user").text.strip()
        print name.encode('gbk')
        if name == config.loginname:
            return True
    return False


"""
    12306验证码
"""


def captcha():
    # 获取验证码
    captcha_data = {
        "login_site": "E",
        "module": "login",
        "rand": "sjrand",
        "0.17231872703389062": ""
    }
    param = urlencode(captcha_data)
    url = config.captcha_url.format(param)
    response = urllib2.urlopen(urllib2.Request(
        url, headers=config.headers))
    if response.getcode() == 200:
        file = BytesIO(response.read())
        img = Image.open(file)
        img.show()

    # 获取验证码输入坐标
    positions = raw_input("输入验证码(以','分割)：".decode('utf-8').encode('gbk'))
    pos = positions.rstrip('\r').strip().split(',')
    temp = ''
    for item in pos:
        temp += config.captcha_point[item] + ','
    pos_res = temp.rstrip(',')
    print pos_res

    # 核对验证码
    captcha_postdata = {
        "answer": pos_res,
        "login_site": "E",
        "rand": "sjrand"
    }
    captcha_postdata = urlencode(captcha_postdata)
    response = urllib2.urlopen(urllib2.Request(config.check_captcha_url,
                                               headers=config.headers2), data=captcha_postdata)
    if response.getcode() == 200:
        result = json.loads(response.read())
        result_message = result.get("result_message")
        result_message = result_message.encode('gbk')
        print result_message
        if result.get("result_code") == "4":
            print "captcha OK"
            return True
        else:
            return False
    return False


def SelectLeftTicket():
    print 'Select LeftTicket'
    response = urllib2.urlopen(urllib2.Request(
        config.left_tickets_sel_init, headers=config.headers))
    # time.sleep(1000)
    # https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date=2018-10-01&leftTicketDTO.from_station=SZQ&leftTicketDTO.to_station=WHN&purpose_codes=ADULT
    left_tickets_url = config.left_tickets_url + \
        'leftTicketDTO.train_date=' + config.Train_Date + \
        '&leftTicketDTO.from_station=' + station.GetStationDict(config.From_Station) + \
        '&leftTicketDTO.to_station=' + station.GetStationDict(config.To_Station) + \
        '&purpose_codes=ADULT'
    print left_tickets_url
    response = urllib2.urlopen(urllib2.Request(
        left_tickets_url, headers=config.headers))
    if response.getcode() == 200:
        r = response.read()
        jdict = json.loads(r)
        raw_trains = jdict['data']
        raw_trains = raw_trains['result']
        pt = PrettyTable()
        pt._set_field_names("车次,车站,时间,经历时,一等座,二等座,软卧,硬卧,硬座,无座".split(','))
        train_dict = []
        for raw_train in raw_trains:
            # split切割之后得到的是一个列表
            data_list = raw_train.split("|")
            dict = {}

            orderurlstr = unquote(data_list[0])
            dict['orderurlstr'] = orderurlstr
            stationTrainCode = data_list[2]
            dict['stationTrainCode'] = stationTrainCode
            train_no = data_list[3]
            dict['train_no'] = train_no
            from_station_code = data_list[6]
            dict['from_station_code'] = from_station_code
            to_station_code = data_list[7]
            dict['to_station_code'] = to_station_code
            from_station_name = station.GetStationName(from_station_code)
            dict['from_station_name'] = from_station_name
            to_station_name = station.GetStationName(to_station_code)
            dict['to_station_name'] = to_station_name
            start_time = data_list[8]
            dict['start_time'] = start_time
            arrive_time = data_list[9]
            dict['arrive_time'] = arrive_time
            time_duration = data_list[10]
            dict['time_duration'] = time_duration
            train_location = data_list[15]
            dict['train_location'] = train_location
            first_class_seat = data_list[31] or "--"
            dict['first_class_seat'] = first_class_seat
            second_class_seat = data_list[30] or "--"
            dict['second_class_seat'] = second_class_seat
            soft_sleep = data_list[23] or "--"
            dict['soft_sleep'] = soft_sleep
            hard_sleep = data_list[28] or "--"
            dict['hard_sleep'] = hard_sleep
            hard_seat = data_list[29] or "--"
            dict['hard_seat'] = hard_seat
            no_seat = data_list[33] or "--"
            dict['no_seat'] = no_seat

            pt.add_row([
                # 对特定文字添加颜色
                train_no,
                '\n'.join([station.GetStationName(from_station_code),
                           station.GetStationName(to_station_code)]),
                '\n'.join([start_time, arrive_time]),
                time_duration,
                first_class_seat,
                second_class_seat,
                soft_sleep,
                hard_sleep,
                hard_seat,
                no_seat
            ])
            train_dict.append(dict)

        # print(pt)
        print train_dict
        return train_dict


def GetSelectTrainInfo(traininfo):
    dictlist = []
    for a in traininfo:
        for b in config.TrainNumber:
            if a['train_no'] == b:
                if config.SeatType == '商务座特等座':
                    pass
                elif config.SeatType == '一等座':
                    if a['first_class_seat'] != u'无' or '*':
                        dictlist.append(a)
                elif config.SeatType == '二等座':
                    if a['second_class_seat'] != u'无' or '*':
                        dictlist.append(a)
                elif config.SeatType == '高级软卧':
                    pass
                elif config.SeatType == '软卧':
                    if a['soft_sleep'] != u'无' or '*':
                        dictlist.append(a)
                elif config.SeatType == '动卧':
                    pass
                elif config.SeatType == '硬卧':
                    if a['hard_sleep'] != u'无' or '*':
                        dictlist.append(a)
                elif config.SeatType == '软座':
                    pass
                elif config.SeatType == '硬座':
                    if a['hard_seat'] != u'无' or '*':
                        dictlist.append(a)
                elif config.SeatType == '无座':
                    if a['no_seat'] != u'无' or '*':
                        dictlist.append(a)
                else:
                    pass
    return dictlist


def CheckUserLogin():
    response = urllib2.urlopen(urllib2.Request(
        config.checkuser_url, headers=config.headers), data=urlencode({"_json_att": ""}))
    if response.getcode() == 200:
        result = json.loads(response.read())
        if result['data']['flag']:
            print('用户在线验证成功'.decode('utf-8').encode('gbk'))
            return True
        else:
            print('检查到用户不在线，请重新登陆'.decode('utf-8').encode('gbk'))
            return False


def SubmitOrder(train_number_str):
    data = {"secretStr": train_number_str,
            "train_date": config.Train_Date,
            "back_train_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "tour_flag": "dc",
            "purpose_codes": "ADULT",
            "query_from_station_name": config.From_Station,
            "query_to_station_name": config.To_Station,
            "undefined": ""
            }
    response = urllib2.urlopen(urllib2.Request(
        config.submit_order_url, headers=config.headers), data=urlencode(data))
    if response.getcode() == 200:
        result = json.loads(response.read())
        if result['status']:
            print('初次提交订单成功'.decode('utf-8').encode('gbk'))
            return True
        elif result['messages'] != []:
            if result['messages'][0] == "车票信息已过期，请重新查询最新车票信息":
                print('车票信息已过期，请重新查询最新车票信息'.decode('utf-8').encode('gbk'))
                return "ticketInfoOutData"
        else:
            print("提交失败".decode('utf-8').encode('gbk'))
            return False


"""
返回3个值：
reSubmitTk,keyIsChange,leftTicketStr
"""


def ConfirmPassenger():
    response = urllib2.urlopen(urllib2.Request(
        config.confirm_passenger_url, headers=config.headers), data=urlencode({"_json_att": ''}))
    if response.getcode() == 200:
        result = response.read()
        try:
            reSubmitTk = re.findall(
                'globalRepeatSubmitToken = \'(\S+?)\'', result)[0]
            keyIsChange = re.findall(
                'key_check_isChange\':\'(\S+?)\'', result)[0]
            leftTicketStr = re.findall('leftTicketStr\':\'(\S+?)\'', result)[0]
            print("获取KEY成功".decode('utf-8').encode('gbk'))
            return reSubmitTk, keyIsChange, leftTicketStr
        except:
            print("获取KEY失败".decode('utf-8').encode('gbk'))
            return 'NetWorkError', 'NetWorkError', 'NetWorkError'


'''
获取所有联系人信息
address=
born_date=1988-00-00 00:00:00
code=9
country_code=CN
email=
first_letter=
gat_born_date=
gat_valid_date_end=
gat_valid_date_start=
gat_version=
index_id=0
mobile_no=155
passenger_flag=0
passenger_id_no=429004
passenger_id_type_code=1
passenger_id_type_name=中国居民身份证
passenger_name=沙
passenger_type=1
passenger_type_name=成人
phone_no=
postalcode=
recordCount=15
sex_code=M
sex_name=男
total_times=99
'''


def GetAllPassengerInfo(reSubmitTk):
    data = {
        "_json_att": "",
        "REPEAT_SUBMIT_TOKEN": reSubmitTk
    }
    response = urllib2.urlopen(urllib2.Request(
        config.get_passenger_url, headers=config.headers), data=urlencode(data))
    if response.getcode() == 200:
        result = json.loads(response.read())

        if result['messages'] != []:
            if result['messages'][0] == '系统忙，请稍后重试':
                return 'systembusy'
        passengerAllInfoList = result['data']['normal_passengers']
        print("获取联系人信息成功".decode('utf-8').encode('gbk'))
        return passengerAllInfoList


def GetTicketPassengerInfo(passengerAllInfoList):
    ticketpassenger = []
    for a in passengerAllInfoList:
        for b in config.TicketName:
            if a['passenger_name'] == b.decode('utf-8'):
                ticketpassenger.append(a)
    print("获取购票人信息成功".decode('utf-8').encode('gbk'))
    return ticketpassenger


def CheckOrderInfo(passengerslist, reSubmitTk):
    passengerTicketStr = ""
    oldPassengerStr = ""
    for item in passengerslist:
        passengerTicketStr += seat.GetSeatType(config.SeatType) + ',0,1,' + \
            item['passenger_name'] + ',1,' + \
            item['passenger_id_no'] + ',' + item['mobile_no'] + ',N_'
        oldPassengerStr += item['passenger_name'] + \
            ',1,' + item['passenger_id_no']+',1_'

    passengerTicketStr = passengerTicketStr.encode('utf-8')
    oldPassengerStr = oldPassengerStr.encode('utf-8')
    data = {
        "cancel_flag": "2",
        "bed_level_order_num": "000000000000000000000000000000",
        "passengerTicketStr": passengerTicketStr,
        "oldPassengerStr": oldPassengerStr,
        "tour_flag": "dc",
        "tour_flag": "dc",
        "randCode": "",
        "whatsSelect": "1",
        "_json_att": "",
        "REPEAT_SUBMIT_TOKEN": reSubmitTk
    }
    response = urllib2.urlopen(urllib2.Request(
        config.check_order_info_url, headers=config.headers), data=urlencode(data))
    if response.getcode() == 200:
        result = json.loads(response.read())
        if result['data']['submitStatus']:
            if result['data']['ifShowPassCode'] == 'N':
                print("checkOrder")
                return True
            if result['data']['ifShowPassCode'] == 'Y':
                GetBuyImage()
                return "Need Random Code"
        else:
            print("checkOrderFail")
            print(result['data']['errMsg'].encode('gbk'))
            return False


'''
1.在这个过程之前，12306会get一张新验证码图片，在购票紧张的时候会在购票时候弹出给你填，如果购票不紧张就不会有但是我们要get到这张图 
2.判断要不要填这个验证的key在上面代码里’ifShowPassCode’ == ‘Y’就是要填，我们要做判断 
这里给出新验证码的获取代码
'''


def GetBuyImage():
    url = config.get_pass_code_new_url + \
        '?module=passenger&rand=randp&{}'.format(random.random())
    response = urllib2.urlopen(urllib2.Request(url, headers=config.headers))
    #file = BytesIO(response.read())
    #img = Image.open(file)
    # img.show()

# 确认订单成功之后，我们就要开始进入购票队列


def GetQueueCount(trainInfo, leftTicketStr):
    thatdaydata = datetime.datetime.strptime(config.Train_Date, "%Y-%m-%d")
    train_date_f = "{} {} {} {} 00:00:00 GMT+0800 (中国标准时间)".format(thatdaydata.strftime('%a'),
                                                                   thatdaydata.strftime(
        '%b'), config.Train_Date.split('-')[2],
        config.Train_Date.split('-')[0])
    data = {
        "train_date": train_date_f,
        "train_no": trainInfo['train_no'],
        "stationTrainCode": trainInfo['stationTrainCode'],
        "seatType": seat.GetSeatType(config.SeatType),
        "fromStationTelecode": trainInfo['from_station_code'],
        "toStationTelecode": trainInfo['to_station_code'],
        "leftTicket": leftTicketStr,
        "purpose_codes": "00",
        "train_location": trainInfo['train_location'],
        "_json_att": "",
        "REPEAT_SUBMIT_TOKEN": reSubmitTk
    }
    response = urllib2.urlopen(urllib2.Request(
        config.get_queue_count_url, headers=config.headers), data=urlencode(data))
    if response.getcode() == 200:
        try:
            result = json.loads(response.read())
        except:
            return "NetWorkError"
    if result['status']:
        print("进入队列成功".decode('utf-8').encode('gbk'))
        return True
    else:
        print("进入队列失败".decode('utf-8').encode('gbk'))
        return False

# 确认单人队列


def ConfirmSingleForQueue(traininfo, passengerslist, keyIsChange, leftTicketStr, reSubmitTk):
    passengerTicketStr = ""
    oldPassengerStr = ""
    for item in passengerslist:
        passengerTicketStr += seat.GetSeatType(config.SeatType) + ',0,1,' + \
            item['passenger_name'] + ',1,' + \
            item['passenger_id_no'] + ',' + item['mobile_no']+',N_'
        oldPassengerStr += item['passenger_name'] + \
            ',1,' + item['passenger_id_no']+',1_'

    passengerTicketStr = passengerTicketStr.encode('utf-8')
    oldPassengerStr = oldPassengerStr.encode('utf-8')
    data = {
        "passengerTicketStr": passengerTicketStr,
        "oldPassengerStr": oldPassengerStr,
        "randCode": "",
        "purpose_codes": "00",
        "key_check_isChange": keyIsChange,
        "leftTicketStr": leftTicketStr,
        "train_location": traininfo['train_location'],
        "choose_seats": "",
        "seatDetailType": "000",
        "whatsSelect": "1",
        "roomType": "00",
        "dwAll": "N",
        "_json_att": "",
        "REPEAT_SUBMIT_TOKEN": reSubmitTk
    }
    response = urllib2.urlopen(urllib2.Request(
        config.confirm_order_url, headers=config.headers), data=urlencode(data))
    if response.getcode() == 200:
        try:
            result = json.loads(response.read())
        except:
            return "NetWorkError"

        if 'data' in result.keys():
            if result['data']['submitStatus'] is True:
                print("确认提交订单成功".decode('utf-8').encode('gbk'))
                return True
            elif result['data']['errMsg'] == u"验证码输入错误！":
                return "wrongCode"

        else:
            print("提交订单失败".decode('utf-8').encode('gbk'))
            return False


def wait_time(reSubmitTk):
    orderId = ''
    url = config.wait_oder_url + '?random={}&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN={}'.format(
        int(time.time()*1000), reSubmitTk)
    response = urllib2.urlopen(urllib2.Request(url, headers=config.headers))
    if response.getcode() == 200:
        try:
            result = json.loads(response.read())
        except:
            return ''
        if result['status']:
            if result['data']['queryOrderWaitTimeStatus']:
                if result['data']['waitTime'] > 0:
                    print result['data']['waitTime']
                    return ''
                elif result['data']['waitTime'] == -1:
                    orderId = result['data']['orderId']
                    print orderId
                    print "请登录12306，完成后续支付"
                    return orderId
                elif result['data']['waitTime'] == -2:
                    print result['data']['msg'].encode('gbk')
                    return 'error'
                else:
                    return 'error'
            else:
                return ''
        else:
            return ''


if __name__ == '__main__':

    if login():
        print('Login Success')
        print('获取站点代码'.decode('utf-8').encode('gbk'))
        station.GetStation()
        GetTicketRes = ''
        TrainSelInfo = []

        while GetTicketRes != 'Suc':
            while TrainSelInfo == []:
                print('查询余票...'.decode('utf-8').encode('gbk'))
                try:
                    TrainAllInfo = SelectLeftTicket()
                    TrainSelInfo = GetSelectTrainInfo(TrainAllInfo)
                except:
                    TrainSelInfo = []
                time.sleep(2)

            for train in TrainSelInfo:
                try:
                    CheckUserLogin()
                    SubmitOrder(train['orderurlstr'])
                    reSubmitTk, keyIsChange, leftTicketStr = ConfirmPassenger()
                    AllPassengerInfo = GetAllPassengerInfo(reSubmitTk)
                    SelPassengerInfo = GetTicketPassengerInfo(AllPassengerInfo)
                    time.sleep(1)
                    # GetBuyImage()
                    CheckOrderInfo(SelPassengerInfo, reSubmitTk)
                    time.sleep(1)
                    GetQueueCount(train, leftTicketStr)
                    time.sleep(1)
                    ConfirmSingleForQueue(
                        train, SelPassengerInfo, keyIsChange, leftTicketStr, reSubmitTk)
                    Timeout = 0
                    while (wait_time(reSubmitTk) == '') or (Timeout < 10):
                        time.sleep(1)
                        Timeout += 1
                    if(Timeout < 10):
                        GetTicketRes = 'Suc'
                        Email.sendmail()
                except Exception, err:
                    print err
            time.sleep(3)
    else:
        print('Failed')
