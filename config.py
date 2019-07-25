# -*- coding: utf-8 -*-
#
# @author: Toso
# @created: Sun Sep 30 2018 14:42:58 GMT+0800 (中国标准时间)
# @comment: ______________
#

# 浏览器headers
headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    "Host": "kyfw.12306.cn",
    "Referer": "https://kyfw.12306.cn/otn/passport?redirect=/otn/"
}

headers2 = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    "Host": "kyfw.12306.cn",
    "Referer": "https://kyfw.12306.cn/otn/login/init"
}

# 12306网址
#########登录###########
init_url = 'https://kyfw.12306.cn/otn/login/init'
captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?{}'
login_url = 'https://kyfw.12306.cn/passport/web/login'
check_captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
uamtk_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
auth_url = 'https://kyfw.12306.cn/otn/uamauthclient'
initmy12306_url = 'https://kyfw.12306.cn/otn/index/initMy12306'
#########查票###########
left_tickets_sel_init = 'https://kyfw.12306.cn/otn/leftTicket/init'
left_tickets_url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?'
#########下单###########
checkuser_url = 'https://kyfw.12306.cn/otn/login/checkUser'
submit_order_url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
confirm_passenger_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
get_passenger_url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
check_order_info_url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
get_queue_count_url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
get_pass_code_new_url = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew'
confirm_order_url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
wait_oder_url = 'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime'
get_result_order_url = 'https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue'
resultOrderForDcQueue = 'https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue'

# 12306验证码地址
captcha_point = {
    '1': '40,43',
    '2': '110,43',
    '3': '180,43',
    '4': '260,43',
    '5': '40,117',
    '6': '110,117',
    '7': '180,117',
    '8': '260,117',
}

##############################################
#需要修改的配置文件
##############################################
# 12306账号信息
logininfo = {
    'username': 'tosobo',               #修改   帐号
    'password': '',           #修改   帐号密码
    'appid': 'otn'
}
loginname = u'沙'                     #修改   帐号名称

#购票信息
From_Station = '武汉'                   #修改    起点站
To_Station = '深圳'                     #修改    终点站
Train_Date = '2019-02-12'               #修改    订票日期
TrainNumber = ['G1007','G1009','G1013','G73','G71','G1015','G79','G1017','']              #修改   车次，为空刷所有
SeatType = '二等座'                     #修改   座次类型
TicketName = ['沙','娟']          #修改   购票人名字

#通知邮箱
Email = 'tosobright@qq.com'             #修改
