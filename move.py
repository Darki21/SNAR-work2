def move(p, U, color_matrix, pExact = 0.8, pOvershoot = 0.1, pUndershoot = 0.1):
    """
    Реализация гипотетического движения с попыткой сохранить данные об окружении

    pExact: Вероятнсть приехать в нужную клетку
    pOvershoot: Вероятнсть перехать клетку
    pUndershoot: Вероятнсть не доехать до клетки
    p: матрица nxn с плотностью вероятности
    U: массив из 2-х чисел 1-ое число смещение по х 2-ое число смещение по у
    pExact: вероятнсть правильного смещения 
    pOvershoot: вероятнсть проехать больше 
    pUndershoot: вероятнсть не доехать 
    return: матрицу с новой вероятностью нахожедния робота в той или иной клетке
    после попытки сдвинутся на U
    """

    # выходим из функции если мы не двигались
    if U[0] == 0 and U[1] == 0:
        return p

    p_new = []
    p_buf = []

    # Такая реалиазция адекватно работает в ТОЛЬКО зациклином мире
    for y in range(len(p)):
        p_buf = []
        for x in range(len(p[y])):

            s = pExact * p[(y - U[1]) % len(p)][(x - U[0]) % len(p[y])]
            # Проверки для понимания куда мы сместились и расчет соответствующий вероятностей(можно сделать лучше)
            # Если двжемся по оси У
            if U[0] == 0:
                s += pOvershoot * p[(y - U[1] - 1) % len(p)][(x - U[0]) % len(p)]
                s += pUndershoot * p[(y - U[1] + 1) % len(p)][(x - U[0]) % len(p)]
                # s += pOvershoot * p[(y - U[1]) % len(p)][(x - U[0] - 1) % len(p[y])]
                # s += pUndershoot * p[(y - U[1]) % len(p)][(x - U[0] + 1) % len(p[y])]
            # Если двжемся по оси Х
            if U[1] == 0:
                s += pOvershoot * p[(y - U[1]) % len(p)][(x - U[0] - 1) % len(p[y])]
                s += pUndershoot * p[(y - U[1]) % len(p)][(x - U[0] + 1) % len(p[y])]
                # s += pOvershoot * p[(y - U[1] - 1) % len(p)][(x - U[0]) % len(p)]
                # s += pUndershoot * p[(y - U[1] + 1) % len(p)][(x - U[0]) % len(p)]
            # Если двжемся по диагонали
            if U[1] != 0 and U[0] != 0:
                s += pOvershoot * p[(y - U[1] - 1) % len(p)][(x - U[0] - 1) % len(p[y])]
                s += pUndershoot * p[(y - U[1] + 1) % len(p)][(x - U[0] + 1) % len(p[y])]
            p_buf.append(round(s, 4))
        p_new.append(p_buf)

        # for i in range(len(p_new)):
        #     for j in range(len(p_new[i])):
        #         if color_matrix[i][j] == 'b':
        #             p_new[i][j] = 0.0
    return p_new
