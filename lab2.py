import random
import numpy as np
import scipy


def get_average(array):
    sum = 0
    for i in range(len(array)):
        sum += array[i]
    return sum / len(array)


def sq1(arr):
    sum = 0
    for i in range(len(arr)):
        sum += arr[i] ** 2
    return 1 / (len(arr) - 1) * sum - get_average(arr) ** 2


def confidence_interval_expectation(arr, t, mean, s):
    n = len(arr)
    left = mean - (t * s / (n ** 0.5))
    right = mean + (t * s / (n ** 0.5))
    return [left, right]


def confidence_interval_sq(arr, xi1, xi2, s):
    n = len(arr)
    left = (n - 1) * (s ** 2) / xi1
    right = (n - 1) * (s ** 2) / xi2
    return [left, right]


def get_t_value(percent, size):
    return abs(scipy.stats.t.ppf((1 - percent) / 2, size - 1))


def get_chi_value(percent, size):
    return scipy.stats.chi2.ppf(percent, size-1)


def calculate(main_array=[], percent=0.95):
    if len(main_array) == 0:
        size = 145
        mean = 10
        variance = 2.2
        np.random.seed(0)
        main_array = np.random.normal(loc=mean, scale=np.sqrt(variance), size=size)
    size = len(main_array)
    t = get_t_value(percent, size)
    s = sq1(main_array) ** 0.5
    average = get_average(main_array)

    left1, right1 = confidence_interval_expectation(main_array, t, average, s)

    xi2 = get_chi_value((1-percent)/2, size - 1)
    xi1 = get_chi_value(1-(1 - percent)/2, size - 1)
    left2, right2 = confidence_interval_sq(main_array, xi1, xi2, s)
    res = {'size': size, 'percent': percent, 'average': average, 'sq': s, 'conf_expectation': [left1, right1],
           'conf_sq': [left2, right2], 't':t, 'xi1':xi1, 'xi2':xi2}
    return res


def print_one(res):
    print("n: " + str(res.get('size')))
    print("%: " + str(res.get('percent')))
    print('t: ' + str(res.get('t')))
    print('xi1: ' + str(res.get('xi1')))
    print('xi2: ' + str(res.get('xi2')))
    print("Середнє значення: " + str(round(res.get('average'), 4)))
    print("Середньоквадратичне відхилення ^1: " + str(round(res.get('sq') ** 0.5, 4)) + ' ^2 ' + str(round(res.get('sq'), 4)))
    print("Математичне сподівання:")
    print(str(res.get('conf_expectation')[0]) + " < u < " + str(res.get('conf_expectation')[1]))
    print("\nСередньоквадратичне відхилення:")
    print(str(res.get('conf_sq')[0]) + " < o^2 < " + str(res.get('conf_sq')[1]))


size = 145
mean = 10
variance = 2.2
np.random.seed(0)
main_array = np.random.normal(loc=mean, scale=np.sqrt(variance), size=size)
main_array1_2 = main_array[:len(main_array) // 2]
main_array1_4 = main_array[:len(main_array1_2) // 2]
main_array1_8 = main_array[:len(main_array1_4) // 2]
main_array1_16 = main_array[:len(main_array1_8) // 2]
main_array1_32 = main_array[:len(main_array1_16) // 2]
main_array1_64 = main_array[:len(main_array1_32) // 2]

arrays = [main_array, main_array1_2, main_array1_4, main_array1_8, main_array1_16, main_array1_32, main_array1_64]
percents = [0.995, 0.99, 0.975, 0.98, 0.95, 0.9, 0.5, 0.2]


def compare(arrays, percents, sortKey='percent', reverse=True):
    res = []
    for array in arrays:
        for percent in percents:
            res.append(calculate(array, percent))
    res.sort(key=lambda x: x.get(sortKey), reverse=reverse)
    print("{:<10} {:<10} {:<50} {:<20}".format('Size', 'Percent', 'Expectation', 'SQ'))
    for re in res:
        size = re.get('size')
        percent = re.get('percent')
        expectation = str(re.get('conf_expectation')[0]) + " < u < " + str(re.get('conf_expectation')[1])
        sq = str(re.get('conf_sq')[0]) + " < o^2 < " + str(re.get('conf_sq')[1])
        print("{:<10} {:<10} {:<50} {:<30}".format(size, percent, expectation, sq))
print(get_chi_value((1-0.9)/2,100))
print_one(calculate(main_array, percent=0.9))
compare(arrays, percents, sortKey='size')