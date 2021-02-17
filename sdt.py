# -*- coding: utf-8 -*-
"""
DateTime    ：2021-02-03
Author      : 俞永庆
Describe    : 处理日期时间类,
Function    :
"""

import datetime
import zhdate as ZhDate
import time
import math

class SDT:
    """
    实现气象日期串相关内容
    """
    

    def __init__(self, **kwargs):
        """
        初始化日期类
        :param kwargs: {sdt:纯数字日期串，dt：time时间}
        """
        print(kwargs)
        if len(kwargs.keys()) == 0:
            self._dt = SDT.toDT()
            self._length = 14
        elif kwargs.__contains__('sdt'):
            self._sdt = kwargs['sdt']
            self._dt = SDT.toDT(self._sdt)
            self._length = len(self._sdt)
        elif kwargs.__contains__('dt'):
            self._dt = kwargs['dt']
            self._length = 14
        else:
            self._dt = time.time()
            self._sdt = SDT.toSDT(self._dt)

    # 属性
    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, value):
        if value > 14:
            value = 14
        elif value < 0:
            value = 0
        self._length = value

    @property
    def sdt(self):
        """
        :return: 日期串
        """
        sdt = SDT.toSDT(self._dt)
        return sdt[:self._length]

    @sdt.setter
    def sdt(self, value):
        if str.isdigit(value):
            value += "00000000000000"  # 不足的用0补全
            # self._sdt = value[0:self._length]
            self._dt = SDT.toDT(self._sdt)
        else:
            raise ValueError('sdt must be all digit!')

    @property
    def dt(self):
        return self._dt

    @dt.setter
    def dt(self, value):
        self._dt = value
        # self._sdt = SDT.toSDT(self._dt)

    @property
    def zhsdt(self):
        # chinese date
        sdt = SDT.toSDT(self._dt)
        d2 = datetime.datetime.strptime(sdt, '%Y%m%d%H%M%S')
        zhdt = ZhDate.ZhDate.from_datetime(d2)
        if zhdt.leap_month:
            return f"{zhdt.lunar_year}-闰{zhdt.lunar_month}-{zhdt.lunar_day}"
        else:
            return f"{zhdt.lunar_year}-{zhdt.lunar_month}-{zhdt.lunar_day}"

    @property
    def eraTime(self):
        # ren hours from 1900-1-1 0:0:0
        dt0 = SDT.toDT("19000101000000")        
        hours = (self.dt - dt0) / 3600 
        return math.floor(hours)
    
    @property
    def necpTime(self):        
        return SDT.toSDT(self._dt)[:10]
    
    # 方法
    def add(self, seconds, **kwargs):
        """
        计算日期串的
        :param seconds: 秒数
        :return: 14位的日期数字串，
        """
        self._dt += seconds
        if kwargs.__contains__('days'):
            self._dt += kwargs['days'] * 86400
        if kwargs.__contains__('hours'):
            self._dt += kwargs['hours'] * 3600
        if kwargs.__contains__('minutes'):
            self._dt += kwargs['minutes'] * 60
        # self._sdt = SDT.toSDT(self._dt)
        return self

    # 静态方法
    @staticmethod
    def toSDT(*args):
        """
        生成日期串，返回14位的
        :param args: 时间
        :return: 14位的日期数字串，
        """
        print('toSDT,args[0]=',args[0])
        
        
        if len(args) == 0:
            return time.strftime("%Y%m%d%H%M%S", time.gmtime())
        else:
            if args[0] < 0:
                days = args[0] / 86400
                days = math.floor(days)
                seconds = args[0] - days * 86400
                dt = datetime.datetime(1970,1,1,0,0,0)
                dt += datetime.timedelta(days=days, seconds=seconds)
                return dt.strftime("%Y%m%d%H%M%S")
            else:
                return time.strftime("%Y%m%d%H%M%S", time.gmtime(args[0]))

    @staticmethod
    def toDT(*args):
        """
        生成时间戳,距离1970-1-1 0：0：0 的秒数
        :param args:
        :return:
        """
        if len(args) == 0:
            return time.time()
        # 字符串转为时间元組
        sdt = args[0]
        if str.isdigit(sdt):
            sdt += "00000000000000"
            sdt = sdt[0:14]
            dt = datetime.datetime.strptime(sdt, "%Y%m%d%H%M%S")
            dt0 = datetime.datetime.strptime('19700101000000', "%Y%m%d%H%M%S")
            td = dt - dt0
            return td.days * 86400 + td.seconds
        else:
            return time.time()
    
    @staticmethod
    def era2necp(eratime):
        """
        change era4time:int to necpTime:str("%Y%m%d%H")     
        """
        hours_off = -25567
        hour_dis = eratime + hours_off
        days = math.floor(hour_dis / 24)
        seconds = hour_dis * 3600 - days * 86400
        dt0 = datetime.datetime(1970, 1, 1, 0, 0, 0)
        dt = dt0 + datetime.timedelta(days=days,seconds=seconds)
        return dt.strftime('%Y%m%d%H')

if __name__ == '__main__':
    print('hello world')
    a = SDT()
    b = SDT(sdt='19580101215954')
    c = SDT(dt = time.time())
    print(c.sdt)
