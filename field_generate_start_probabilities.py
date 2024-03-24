def field_generate_start_probabilities(x, y):
    """
    Генерирует равномерное распределение для поля размером x на y клеток.

    :param x: кол-во клеток (ширина)
    :param y: кол-во клеток (длина)
    :return p: матрица размером (x, y) с равномерным распеределением вероятностей
    """

    # вероятность попадания в клетку
    # робот только заспавнился => он не может скзаать, где он => он в любой клетке может оказаться с одним шансом
    # шанс = 1/общее кол-во клеток

    number_of_tiles = x*y

    p = list()
    for i in range(x):
        sub_list = list()
        for j in range(y):
            sub_list.append(round(1/number_of_tiles, 3))
        p.append(sub_list)

    return p
