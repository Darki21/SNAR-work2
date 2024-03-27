def field_generate_start_probabilities(rows, columns, color_matrix):
    """
    Генерирует равномерное распределение для поля размером x на y клеток.
    :wall_count: кол-во стенок
    :param rows: кол-во строк матрицы
    :param columns: кол-во столбцов матрицы
    :return p: матрица размером (rows, columns) с равномерным распеределением вероятностей
    """

    # вероятность попадания в клетку
    # робот только заспавнился => он не может скзаать, где он => он в любой, кроме стенок, клетке может оказаться с одним шансом
    # шанс = 1/общее кол-во свободных клеток

    wall_count = 0

    for y in range(len(color_matrix)):
        wall_count += color_matrix[y].count('b')

    number_of_tiles = rows * columns - wall_count

    p = list()
    for i in range(rows):
        sub_list = list()
        for j in range(columns):
            if color_matrix[i][j] == 'b':
                sub_list.append(0.0)
            else:
                sub_list.append(round(1/number_of_tiles, 3))
        p.append(sub_list)

    return p
