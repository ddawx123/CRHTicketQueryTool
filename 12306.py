# !/user/bin/env python
# -*- coding:utf-8 -*-
import sys
import requests
import time
import ssl
from urllib import parse
import urllib3

urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context
req = requests.Session()

class leftQuery(object):
    '''余票查询入口'''
    def __init__(self):
        self.station_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
        self.headers = {
            'Host': 'kyfw.12306.cn',
            'If-Modified-Since': '0',
            'Pragma': 'no-cache',
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def station_name(self, station):
        '''读取车站列表'''
        html = requests.get(self.station_url, verify=False).text
        result = html.split('@')[1:]
        dict = {}
        for i in result:
            key = str(i.split('|')[1])
            value = str(i.split('|')[2])
            dict[key] = value
        if (station in dict.keys()):
            return dict[station]
        else:
            print('抱歉，站点名称：“' + station + '”无效。请重新提供有效的站点名！')
            sys.exit(0)

    def query(self, from_station, to_station, date):
        '''余票查询方法'''
        fromstation = self.station_name(from_station)
        tostation = self.station_name(to_station)
        url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
            date, fromstation, tostation)
        try:
            html = requests.get(url, headers=self.headers, verify=False).json()
            result = html['data']['result']
            if result == []:
                print('很抱歉,没有查到符合当前条件的列车!')
                exit()
            else:
                print(date + ' 【' + from_station + '->' + to_station + '】 车票实时信息查询成功！\n')
                num = 1
                for i in result:
                    info = i.split('|')
                    if info[0] != '' and info[0] != 'null':
                        print(str(num) + '.' + info[3] + '车次还有余票:')
                        print('出发时间:' + info[8] + ' 到达时间:' + info[9] + ' 历时多久:' + info[10] + ' ', end='')
                        seat = {21: '高级软卧', 23: '软卧', 26: '无座', 28: '硬卧', 29: '硬座', 30: '二等座', 31: '一等座', 32: '商务座',
                                33: '动卧'}
                        from_station_no = info[16]
                        to_station_no = info[17]
                        for j in seat.keys():
                            if info[j] != '无' and info[j] != '':
                                if info[j] == '有':
                                    print(seat[j] + ':有票 ', end='')
                                else:
                                    print(seat[j] + ':有' + info[j] + '张票 ', end='')
                        print('\n')
                    elif info[1] == '预订':
                        print(str(num) + '.' + info[3] + '车次暂时没有余票\n')
                    elif info[1] == '列车停运':
                        print(str(num) + '.' + info[3] + '车次列车停运\n')
                    elif info[1] == '23:00-06:00系统维护时间':
                        print(str(num) + '.' + info[3] + '23:00-06:00系统维护时间\n')
                    else:
                        print(str(num) + '.' + info[3] + '车次列车运行图调整,暂停发售\n')
                    num += 1
            return result
        except:
            print('查询信息失败，建议检查数据合法性后重试！')
            exit()

def scan():
    if (len(sys.argv) == 4):
    	from_station = sys.argv[1].strip()
    	to_station = sys.argv[2].strip()
    	date = sys.argv[3].strip()
    	result = leftQuery().query(from_station, to_station, date)
    else:
    	from_station = input('键入您要购票的出发站点(Example: 杭州东)：').strip()
    	to_station = input('键入您要购票的目的站点(Example: 绍兴北)：').strip()
    	date = input('键入您的乘车日期(Example: 2019-01-10)：').strip()
    	result = leftQuery().query(from_station, to_station, date)

if __name__ == '__main__':
    print('*' * 20 + '【小丁工作室】春运抢票监控系统 V2019.1' + '*' * 20 + '\n')
    print('服务器时间：' + time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time())) + '\n')
    scan()
