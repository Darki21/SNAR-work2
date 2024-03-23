def sense(p, Z, world, pHit = 0.6, pMiss = 0.2):
    """
    Вычисляет апосториорную(инфа псоле полчуния показания с датчиков) матрицу вероятности

    p: двумереый массив nxn с плотностью распределения
    Z: Показание с датчика в виде одной буквы
    world: двумереый массив nxn с значениями цветов клеток на крате
    pHit: 
    pMiss:

    return: матрицу с новой вероятностью нахожедния робота в той или иной клетке
    """

    p_new   = []
    p_buf   = []
    buf_sum = []

    for i in range(len(p)):
        p_buf = []

        for j in range(len(p[i])):
            hit = (Z == world[i][j])
            p_buf.append(p[i][j]*(hit*pHit + (1-hit)*pMiss))

        p_new.append(p_buf)
        buf_sum.append(sum(p_buf))

    totla_sum = sum(buf_sum)

    for i in range(len(p)):
        for j in range(len(p[i])):
            p_new[i][j] = round(p_new[i][j]/totla_sum, 3)
    return p_new
