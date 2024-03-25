def field_generate_start_probabilities(rows, columns):
    """
    Генерирует равномерное распределение для поля размером x на y клеток.

    :param rows: кол-во строк матрицы
    :param columns: кол-во столбцов матрицы
    :return p: матрица размером (rows, columns) с равномерным распеределением вероятностей
    """

    # вероятность попадания в клетку
    # робот только заспавнился => он не может скзаать, где он => он в любой клетке может оказаться с одним шансом
    # шанс = 1/общее кол-во клеток

    number_of_tiles = rows * columns

    p = list()
    for i in range(rows):
        sub_list = list()
        for j in range(columns):
            sub_list.append(round(1/number_of_tiles, 3))
        p.append(sub_list)

    return p
