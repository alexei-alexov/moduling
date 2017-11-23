# -*- coding: utf-8 -*-
from random import uniform


def system_with_recall_sources(m, c, mu, nu, la):
    r = [[] for _ in range(m + 1)]
    r[m].extend([1, 1])

    for i in range(2, c + 1):
        r[m].append(((la + (i - 1) * nu + m * mu) * r[m][i - 1] - la * r[m][i - 2]) / (i * nu))

    for j in range(m - 1, -1, -1):
        b, d = [0], [0]
        r[j].extend([0 for _ in range(c + 1)])

        for i in range(1, c + 1):
            b.append(i * nu * (j * mu + b[i - 1]) / (la + j * mu + b[i - 1]))
            d.append((j + 1) * mu * r[j + 1][i - 1] + (la * d[i - 1]) / (la + j * mu + b[i - 1]))

        r[j][c] = (j + 1) * mu * sum(r[j + 1][0:c]) / la

        for i in range(c - 1, -1, -1):
            r[j][i] = (d[i] + (i + 1) * nu * r[j][i + 1]) / (la + j * mu + b[i])

    pi0m = 1 / sum(map(sum, r))
    pi = [[ri * pi0m for ri in rj] for rj in r]
    pi[m][0] = pi0m

    average_busy_equipment = sum([i * sum(map(lambda pij: pij[i], pi)) for i in range(1, c + 1)])
    average_recall_sources = sum([j * sum(pi[j]) for j in range(1, m + 1)])
    average_time_from_call_to_service = average_recall_sources / la
    loss_call_probability = sum(map(lambda pij: pij[c], pi))

    return (
        average_busy_equipment,
        average_recall_sources,
        average_time_from_call_to_service,
        loss_call_probability
    )


def main():
    import sys

    try:
        if len(sys.argv) > 1:
            la, c, m, test_amount = (int(i) for i in sys.argv[1:])
        else:
            la = int(input("Введіть інтенсиність потоку: "))
            c = int(input("Введіть кількість приладів: "))
            m = int(input("Введіть кількість джерел повторних викликів: "))
            test_amount = int(input("Введіть кількість тестів: "))
    except:
        return

    average_busy_equipment_total = []
    average_recall_sources_total = []
    average_time_from_call_to_service_total = []
    loss_call_probability_total = []

    for test in range(test_amount):
        nu = uniform(0, 0.5)  # serving_time
        mu = uniform(0, 0.5)  # recall_time

        print("Тест #%s\nЧас обслуговування: %s\nЧас повторного виклику: %s" % (test, round(nu * 60, 2), round(mu * 60, 2)))

        (
            average_busy_equipment,
            average_recall_sources,
            average_time_from_call_to_service,
            loss_call_probability
        ) = system_with_recall_sources(m, c, mu, nu, la)
        
        average_busy_equipment_total.append(average_busy_equipment)
        average_recall_sources_total.append(average_recall_sources)
        average_time_from_call_to_service_total.append(average_time_from_call_to_service)
        loss_call_probability_total.append(loss_call_probability)

        print('Середня кількість зайнятих приладів: ', round(average_busy_equipment, 2))
        print('Середня зайнятість повторної черги: ', round(average_recall_sources, 2))
        print('Середній час очікування первинного виклику: ', round(average_time_from_call_to_service * 60, 3))
        print('Ймовірність втрати первинного виклику: ', round(loss_call_probability, 2), '\n')
    
    print('## Результат виконання всіх тестів ##')
    print('## Середня кількість зайнятих приладів:        %5s ##' % (round(sum(average_busy_equipment_total) / test_amount, 2)))
    print('## Середня зайнятість повторної черги:         %5s ##' % (round(sum(average_recall_sources_total) / test_amount, 2)))
    print('## Середній час очікування первинного виклику: %5s ##' % (round(sum(average_time_from_call_to_service_total * 60) / test_amount, 3)))
    print('## Ймовірність втрати первинного виклику:      %5s ##' % (round(sum(loss_call_probability_total) / test_amount, 2) ))


if __name__ == '__main__':
    main()
