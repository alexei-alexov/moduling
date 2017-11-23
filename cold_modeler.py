from math import ceil, log, factorial as fact

STREAM_TYPES = (
    "M", "D", "Ek", "GI", "G",
)

QUEUE_DISCIPLINE_TYPES = (
    "FCFS", "LCFS", "SIRO", "GD",
)

HOUR = 60

T1_STRS = (
    """
Пацієнти прибувають на прийом до лікаря відповідно до розподілу Пуассона із інтенсивністю
8 пацієнтів за годину. Час огляду клієнта є показниково розподілена випадкова величина із
середнім значенням 9 пацієнтів за годину. Пацієнти можуть чекати на прийом як в кімнаті
для очікування так і за її межами.
    """,
    "Ймовірність того, що пацієнт, який прибув не буде чекати: %s",
    "Середню кількість пацієнтів, що очікують на прийом: %s",
    "Середній час очікування пацієнта від моменту прибуття до початку прийому: %s",
    "Середній час, який витрачений пацієнтом на перебування в поліклініці: %s",
    "Ймовірність того, що пацієнт, який прибуде до лікаря, матиме можливість очікувати на стільчику (в кімнаті для очікування є 12 стільчиків): %s"
)

T2_STRS = (
    """
В перукарні є 1 перукар. Клієнти прибувають відповідно до розподілу Пуассона в середньому
4 чол. на годину. Час обслуговування розподілений за показниковим розподілом та становить
в середньому 20 хвилин. Місць для очікування в залі всього 3. Нові клієнти, які приходять
до перукарні, при відсутності місць для очікування, ідуть у пошуках іншої перукарні.
    """,
    "Ефективну інтенсивність надходження клієнтів до системи: %s",
    "Середню кількість клієнтів, що очікують на обслуговування: %s",
    "Середній час очікування клієнта від моменту прибуття до початку обслуговування: %s",
    "Середній час, який витрачений на перебування клієнта в перукарні: %s",
    "Ймовірність того, що клієнт, який зайде до перукарні та побачить, що всі місця зайняті, піде в пошуках іншої перукарні: %s"
)

T3_STRS = (
    """
У невеликому місті функціонує одна служба таксі, яка має чотири автомобілі.
Замовлення до диспетчерських відділень надходять із однаковою інтенсивністю,
яка становить в середньому 16 викликів на годину. Середній час виконання
одного замовлення складає 12 хвилин. Замовлення на обслуговування надходять
відповідно до розподілу Пуассона, а час обслуговування вимог має показниковий розподіл.
    """,
    "Ймовірність того, що всі автомобілі служби на виклику: %s",
    "Середню кількість вимог, які очікують на прибуття: %s",
    "Середній час очікування клієнтом прибуття автомобіля(очікування в черзі): %s",
    "Кількість автомобілів, яку слід мати компанії для того, щоб тривалість очікування клієнтом приїзду автомобіля становила не більше 5 хвилин: %s",
    "Середню кількість вільних автомобілів: %s",
)

T4_STRS = (
    """
Автостоянка біля магазину має 5 місць. Автомобілі прибувають на стоянку відповідно до розподілу Пуассона із
інтенсивністю 6 автомобілів в годину. Час перебування автомобілів на стоянці є показниково розподіленою
випадковою величиною із середнім 30 хв. Автомобілі можуть очікувати, коли звільниться місця на стоянці на
пішохідних доріжках в кількості 5 автомобілів. Водії при відсутності місць на стоянці та місць для очікування
повинні шукати інші стоянки.
    """,
    "Ефективну інтенсивність надходження клієнтів до системи: %s",
    "Ймовірність того, що всі місця на стоянці будуть вільними: %s",
    "Середню кількість автомобілів, які знаходяться в системі: %s",
    "Середню кількість автомобілів, які очікують на звільнення місця на стоянці: %s",
)


def ppercent(f):
    return "%.2f%%" % (f * 100, )


def get_p(l, m):
    return l / m


# def avg_client_in_system_amount():
#     """Ls"""
#     pass

# def avg_client_in_queue_amount():
#     """Lq"""
#     pass

# def avg_time_in_system():
#     """Ws"""
#     pass


# def avg_time_in_queue():
#     """Wq"""
#     pass

# def avg_busy_services():
#     """cb"""
#     pass

# def get_client_in_system_chance():
#     return n * p(n)

def task1():
    print(T1_STRS[0])
    l = 8
    m = 9
    p = get_p(l, m)
    
    chairs = 12
    N = 1 + chairs
    
    wont_wait_chance = 1 - ( (1 - p) * (1 - p**(1+1)) / (1 - p) )
    avg_wait_amount = pow(p, 2) / (1 - p)
    avg_queue_wait = p / (m * (1 - p))
    avg_system_using = 1 / (m - l)
    
    queue_avail_chance = (1 - p) * (p ** (N - 1)) / (1 - p ** (N + 1))

    print(T1_STRS[1] % (ppercent(wont_wait_chance), ))
    print(T1_STRS[2] % (round(avg_wait_amount), ))
    print(T1_STRS[3] % (round(avg_queue_wait, 2), ))
    print(T1_STRS[4] % (round(avg_system_using, 2), ))
    print(T1_STRS[5] % (ppercent(p ** N), ))


def task2():
    print(T2_STRS[0])
    l = 4
    service_time = 20
    m = HOUR // service_time
    p = get_p(l, m)

    queue_size = 3
    N = queue_size + 1

    def get_p_chance(n):
        return (1 - p) * (p ** n) / (1 - (p ** (n+1)))

    
    lose_chance = get_p_chance(N)
    effective_intensity = l - l*lose_chance
    avg_wait_amount = p * (1 - (N+1)*(p**N) + N*(p**(N+1))) / ((1 - p) * (1 - p**(N+1)))
    time_spent = avg_wait_amount / effective_intensity
    effective_time_spent = time_spent - (1 / m) 
    

    print(T2_STRS[1] % (round(effective_intensity), ))
    print(T2_STRS[2] % (avg_wait_amount, ))
    print(T2_STRS[3] % (round(effective_time_spent, 2), ))
    print(T2_STRS[4] % (round(time_spent, 2), ))
    print(T2_STRS[5] % (ppercent(lose_chance), ))

def task3():
    print(T3_STRS[0])
    l = 16
    service_time = 12
    m = HOUR // service_time
    car_amount = 4
    N = car_amount
    c = car_amount
    p = get_p(l, m)
    
    def get_shared_part(n):
        return (sum((p**i) / fact(i) for i in range(N)) + ((p ** N) / (fact(N)))* (1 / (1 - (p / N)))) ** -1

    def get_p_chance(n):
        if n <= N:
            return ((p**n) / fact(n)) * get_shared_part(n)
        else:
            return ((p**n) / (fact(N) * N ** (n - N))) * get_shared_part(n)

    empty_chance = get_p_chance(0)

    def count_lq(c):
        return empty_chance * (p ** (c+1)) / (fact(c - 1) * (c - p)**2)
    
    lq = avg_client_in_queue_amount = count_lq(c)
    # avg_client_in_system_amount = avg_client_in_queue_amount + p

    wq = avg_client_in_queue_time = avg_client_in_queue_amount / l
    # avg_client_in_system_time = avg_client_in_system_amount / 1

    target_car_amount = c+1
    while count_lq(target_car_amount) / l > (5 / 60):
        target_car_amount += 1

    print(T3_STRS[1] % (get_p_chance(4), ))
    print(T3_STRS[2] % (avg_client_in_queue_amount, ))
    print(T3_STRS[3] % (avg_client_in_queue_time, ))
    print(T3_STRS[4] % (target_car_amount, ))
    print(T3_STRS[5] % (c - avg_client_in_queue_amount, ))


def task4():
    print(T4_STRS[0])
    l = 6
    service_time = 30
    m = HOUR // service_time

    c = 5
    queue = 5
    N = c + queue

    p = get_p(l, m)
    p_sum = sum((p**i) / fact(i) for i in range(c))
    
    p0 = p_sum + (p ** c) * (1 - (p/c)**(N - c +1)) / ((fact(c)) * (1 - (p/c)))
    p0 = 1 / p0
    def get_p_chance(n):
        if n < c:
            return p0 * (p ** n) / fact(n)
        else:
            return p0 * (p ** n) / (fact(c) * (c ** (n - c)))

    effective_intensity = l * (1 - get_p_chance(N))


    avg_client_in_queue_amount = p0 * ((p ** (c+1)) / (fact(c-1)*((c-p)**2))) * (1 - pow(p/c, N-c+1) - (N-c+1)*(1-p/c)*pow(p/c, N-c)) 
    avg_client_in_system_amount = avg_client_in_queue_amount + effective_intensity / m

    print(T4_STRS[1] % (effective_intensity, ))
    print(T4_STRS[2] % (ppercent(get_p_chance(0)), ))
    print(T4_STRS[3] % (avg_client_in_system_amount, ))
    print(T4_STRS[4] % (avg_client_in_queue_amount, ))

def infinite_queue(l, service_time):
    m = HOUR / service_time
    p = l / m

    def pi(k):
        return (p**k) * (1-p)

    def pi_chance(s):
        return (1 - p) * (1 - p**(s+1)) / (1 - p)

    avg_wait_amount = pow(p, 2) / (1 - p)

    free_chance = 0.9
    busy_chance = 1.0 - free_chance
    s = ceil(log(busy_chance, p) - 1)

    avg_system_using = 1 / (m - l)
    avg_queue_wait = p / (m * (1 - p))
    avg_task_in_system = p / (1 - p)


    print(s)
    print(ppercent(avg_system_using))
    print(ppercent(avg_queue_wait))
    print(ceil(avg_task_in_system))
    print(ppercent(pi_chance(0)))
    print(ppercent(pi_chance(1)))
    print()

def main():
    try:
        
        n = int(input("Enter task to solve:"))
        {
            1: task1,
            2: task2,
            3: task3,
            4: task4,
        }[n]()
        
    except Exception as err: print(err)
    # infinite_queue(l = 4, service_time = 10)
    
    
    
if __name__ == "__main__":
    main()


