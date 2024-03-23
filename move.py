def move(p, U, pExact = 0.8, pOvershoot = 0.1, pUndershoot = 0.1):
    """
    Реализация гипотетического движения с попыткой сохранить данные об окружении

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
    for i in range(len(p)):
        p_buf = []
        for j in range(len(p[i])):

            s = round(pExact * p[(i - U[1]) % len(p)][(j - U[0]) % len(p[i])], 3)
            # Проверки для понимания куда мы сместились и расчет соответствующий вероятностей(можно сделать лучше)
            # Если двжемся по оси У
            if U[0] == 0:
                s += round(pOvershoot * p[(i - U[1] - 1) % len(p)][(j - U[0]) % len(p)], 3)
                s += round(pUndershoot * p[(i - U[1] + 1) % len(p)][(j - U[0]) % len(p)], 3)
            # Если двжемся по оси Х
            if U[1] == 0:
                s += round(pOvershoot * p[(i - U[1]) % len(p)][(j - U[0] - 1) % len(p)], 3)
                s += round(pUndershoot * p[(i - U[1]) % len(p)][(j - U[0] + 1) % len(p)], 3)
            # Если двжемся по диагонали
            if U[1] != 0 and U[0] != 0:
                s += round(pOvershoot * p[(i - U[1] - 1) % len(p)][(j - U[0] - 1) % len(p)], 3)
                s += round(pUndershoot * p[(i - U[1] + 1) % len(p)][(j - U[0] + 1) % len(p)], 3)
            p_buf.append(s)
        p_new.append(p_buf)
    return p_new
