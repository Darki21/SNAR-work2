from random import random

def field_generate_colour(x, y):
    """
    Гененрирует карту распределения цвета на поле размером (x, y) клеток

    :param x: кол-во клеток (ширина)
    :param y: кол-во клеток (длина)
    :return colour_map: матрица размером (x, y) с отметками цвета (r или g)
    """

    colour_map = list()
    for i in range(x):
        sub_list = list()
        for j in range(y):
            random_number = random()
            if random_number >= 0.5:
                sub_list.append('r')
            else:
                sub_list.append('g')
        colour_map.append(sub_list)

    return colour_map
