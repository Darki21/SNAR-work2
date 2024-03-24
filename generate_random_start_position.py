from random import randint


def generate_random_start_position(x, y):
    """
    Вычисляет случайную точку на поле размером (x, y), где заспавнится робот. Нужно учитывать, что ось Ox идёт вправо,
    а ось Oy -- вниз.

    :param x: размер поля (ширина)
    :param y: размер поля (высота)
    :return pos: список из двух индексов (первый индекс -- индекс клетки относительно оси Ox, второй -- оси Oy)
    """

    pos = list()
    pos.append(randint(0, x-1))
    pos.append(randint(0, y-1))
    return pos
