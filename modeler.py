from math import log
import random


class Stream(object):

    def __init__(self, param, generator):
        self.param = param
        self.generator = generator
        self.reset()

    def reset(self):
        self.time = 0

    def get(self):
        d = (1 / param) * log(generator)
        self.time += d
        return d


class SingleDeviceSystem(object):

    def __init__(self, in_stream, serv_stream):
        self.in_stream = in_stream
        self.serv_stream = serv_stream

    def test(self, time):
        t = 0
        # reset orders data
        orders = 1
        served_orders = 1
        # starting time 0
        self.in_stream.reset()
        self.serv_stream.reset()
        # 
        while in_stream.time < time:
            serv_delta = self.serv_stream.get()
            order_delta = self.in_stream.get()
            orders += 1
            if self.in_stream.time >= self.serv_stream.time:
                served_orders +=
        print("orders: {} served: {}".format(orders, served_orders))


if __name__ == "__main__":
    T = int(input("Enter T: "))
    k = int(input("Enter k: "))

    iu = float(input("Enter input stream param: "))
    su = float(input("Enter service stream param: "))

    in_s

        
