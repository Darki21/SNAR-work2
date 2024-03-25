from time import localtime


def take_system_time():
    """
    Определяет текущее системное время и записывает его значение в строку.

    :param: None
    :return time: строка со временем в формате чч:мм:сс
    """

    time_current = localtime()

    time = str(time_current.tm_hour)
    time += ':'
    time += str(time_current.tm_min)
    time += ':'
    time += str(time_current.tm_sec)

    return time

