from random import random
import numpy as np


# поле с клетками, размер задан пользователем, раскидывает цвета по клеткам
def field_generate_colour(x, y):
    """
    Распределяет случайным образом цвета (red, green) по клеткам.

    :param x: кол-во клеток в ширину
    :param y: кол-во клеток в высоту

    return field_colored: матрица, где каждой клетке поля сопоставлен цвет
    """

    # инициализация field_colored
    field_colored = np.empty((x, y), dtype=str)

    # принцип генерации: береём случайное число, если оно равно или больше 0.5, то клетка красная
    # в противном случае клетка зелёнка

    for i in range(x):
        for j in range(y):
            random_number = random()
            if random_number >= 0.5:
                field_colored[i][j] = 'r'
            else:
                field_colored[i][j] = 'g'

    return field_colored
