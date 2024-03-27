from random import randint


def generate_random_start_position(rows, columns, c):
    """
    Вычисляет случайную точку на матрице размером (y, x), где заспавнится робот.
    Нужно учитывать, что ось Ox идёт вправо, а ось Oy -- вниз (потому что tkinter так работает).

    :param rows: кол-во строк (размер поля в высоту)
    :param columns: кол-во столбцов (размер поля в ширину)
    :param c: карта мира (отражает распределение цветов)
    :return pos: список из двух индексов (первый индекс -- индекс клетки относительно оси Ox, второй -- оси Oy)
    """

    # формирование списка запретных для спавна зон (потому что там стенки)
    # списков из списков
    # один подсписок -- индексы элемента матрицы (карты), где находится стенка
    # NB сначала идут индексы СТОЛБЦОВ, потом -- СТРОК, почему: потому что такой порядок у переменных,
    # характеризующих позицию робота
    where_cannot_spawn = []
    for i in range(rows):
        for j in range(columns):
            if c[i][j] == 'b':
                where_cannot_spawn_tile = []
                tile_row_number = i
                tile_column_number = j
                where_cannot_spawn_tile.append(tile_column_number)
                where_cannot_spawn_tile.append(tile_row_number)
                where_cannot_spawn.append(where_cannot_spawn_tile)


    print("Где нельзя спавниться: ")
    print(where_cannot_spawn)

    is_spawn_pont_good = False

    # такой порядок, потому что если речь идёт про позицию робота, сначала задаётся по Ox
    # (= по ширине поля = по кол-ву СТОЛБЦОВ), а уже потом -- по Oy (= по высоте поля = по кол-ву СТРОК)
    # NB в чём проблема: не покрыт случай, когда у нас совершенно внезапно стенками заполнено ВСЁ поле. Тогда функция
    # будет в вечном цикле. Но при тестировании основной программы таких случаев не было замечено, поэтому
    # оставлено так
    while not is_spawn_pont_good:
        pos = list()
        spawn_point_column_index = randint(0, columns - 1)
        spawn_point_row_index = randint(0, rows - 1)
        pos.append(spawn_point_column_index)
        pos.append(spawn_point_row_index)
        if pos not in where_cannot_spawn:
            is_spawn_pont_good = True

    return pos
