from math import log
import random


TABLE_FORMAT = '|{:^3}|{:^6.2f}|{:^6.2f}|{:^6.2f}|{:1}|{:1}|'


def round(n, p=2):
    return float(int(n*(10**p))) / (10**p) or 0.01


class Stream(object):

    def __init__(self, param, generator):
        self.param = param
        self.generator = generator
        self.reset()

    def reset(self):
        self.time = 0

    def get(self):
        d = round( - (1 / self.param) * log(round(self.generator.random())))
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
        serv_start = 0
        served = True
        
        # starting time 0
        self.in_stream.reset()
        self.serv_stream.reset()

        # serving first order
        serv_delta = self.serv_stream.get()
        service_time = [serv_delta]
        # 
        print('-'*len(TABLE_FORMAT))
        print(TABLE_FORMAT.format(orders, self.in_stream.time, serv_start, self.serv_stream.time, int(served), int(not served)))
        
        while self.in_stream.time < time:

            serv_start = 0
            served = False
            order_delta = self.in_stream.get()
            orders += 1
            # print('{} - {}'.format(self.in_stream.time, self.serv_stream.time))
            if self.in_stream.time >= self.serv_stream.time:
                served = True
                self.serv_stream.time = serv_start = self.in_stream.time
                serv_delta = self.serv_stream.get()
                served_orders += 1
                service_time.append(serv_delta)

            print(TABLE_FORMAT.format(orders, self.in_stream.time, serv_start, self.serv_stream.time, int(served), int(not served)))
        print('Кількість замовлень: {}\nКількість замовлень які отримали обслуговування: {}'. format(orders, served_orders))
        return (orders, served_orders, service_time)


if __name__ == "__main__":
    T = int(input("Enter T: "))
    k = int(input("Enter k: "))

    iu = float(input("Enter input stream param: "))
    su = float(input("Enter service stream param: "))

    input_stream = Stream(iu, random)
    service_stream = Stream(su, random)

    system = SingleDeviceSystem(input_stream, service_stream)

    run_results = []
    service_times = []

    for _ in range(k):
        run_result = system.test(T)
        service_times.extend(run_result[2])
        run_results.append(run_result)
    
    served_orders = sum(result[1] for result in run_results)
    all_orders = sum(result[0] for result in run_results)

    avg_get_served = served_orders / k
    avg_orders = all_orders / k
    avg_service_time = sum(service_times) / len(service_times)

    get_served_chance = served_orders / all_orders
    service_denie_chance = (all_orders - served_orders) / all_orders

    print("------------------------------------\nРезультат тесту\n------------------------------------")
    print("Кількість тестів: {}".format(k))
    print("Середнє число вимог: {}".format(avg_orders))
    print("Середнє число вимог, що отримали обслуговування: {}".format(avg_get_served))
    print("Середній час обслуговування однієї вимоги: {}".format(avg_service_time))
    print("Ймовірність обслуговування: {}".format(get_served_chance))
    print("Ймовірність відмови: {}".format(service_denie_chance))
    


        
