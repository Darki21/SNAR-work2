from random import random


def field_generate_colour(rows, columns):
    """
    Генерирует карту распределения цвета на матрицу размером (rows, columns) клеток

    :param rows: кол-во строк матрицы
    :param columns: кол-во столбцов матрицы
    :return colour_map: матрица размером (rows, columns) с отметками цвета (r или g)
    """

    colour_map = list()
    for i in range(rows):
        sub_list = list()
        for j in range(columns):
            random_number = random()
            if random_number <= 0.45:
                sub_list.append('r')
            elif random_number <= 0.9:
                sub_list.append('g')
            else:
                sub_list.append('b')
        colour_map.append(sub_list)

    return colour_map
