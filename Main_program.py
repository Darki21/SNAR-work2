import random


def sense(p, Z):
    """
    Вычисляет апосториорную(инфа псоле полчуния показания с датчиков) матрицу вероятности
    p: двумереый массив nxn с плотностью распределения 
    Z: Показание с датчика в виде одной буквы 
    return: матрицу с новой вероятностью нахожедния робота в той или иной клетке 
    """

    p_new   = []
    p_buf   = []
    buf_sum = []
    pHit    = 0.6
    pMiss   = 0.2

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
            p_new[i][j] =  p_new[i][j]/totla_sum
    return p_new

def move(p, U):
    """
    Реализация гипотетического движения с попыткой сохранить данные об окружении
    
    p: матрица nxn с плотностью вероятности 
    U: массив из 2-х чисел 1-ое число смещение по х 2-ое число смещение по у
    return: матрицу с новой вероятностью нахожедния робота в той или иной клетке
    после попытки сдвинутся на U
    """

    #выходим из функции если мы не двигались 
    if U[0] == 0 and U[1] == 0:
        return p
    
    p_new = []
    p_buf = []
    pExact      = 0.8
    pOvershoot  = 0.1
    pUndershoot = 0.1
    # Такая реалиазция адекватно работает в ТОЛЬКО зациклином мире
    for i in range(len(p)):
        p_buf = []
        for j in range(len(p[i])):
            
            s = pExact*p[(i-U[1]) % len(p)][(j-U[0]) % len(p[i])]
            #Проверки для понимания куда мы сместились и расчет соответствующий вероятностей(можно сделать лучше)
            #Если двжемся по оси У 
            if U[0] == 0:
                s += pOvershoot*p[(i-U[1]-1) % len(p)][(j-U[0]) % len(p)]
                s += pUndershoot*p[(i-U[1]+1) % len(p)][(j-U[0]) % len(p)]
            #Если двжемся по оси Х
            if U[1] == 0:
                s += pOvershoot*p[(i-U[1]) % len(p)][(j-U[0]-1) % len(p)]
                s += pUndershoot*p[(i-U[1]) % len(p)][(j-U[0]+1) % len(p)]
            #Если двжемся по диагонали 
            if U[1] != 0 and U[0] != 0:
                s += pOvershoot*p[(i-U[1]-1) % len(p)][(j-U[0]-1) % len(p)]
                s += pUndershoot*p[(i-U[1]+1) % len(p)][(j-U[0]+1) % len(p)]
            p_buf.append(s)
        p_new.append(p_buf)
    return p_new
        
def argmax(values):
    """
    values: матрица nxn с плотностью вероятности
    """
    y = max(enumerate(values), key=lambda x: x[1])[0]
    x = max(enumerate(values[y]), key=lambda x: x[1])[0]

    return [x, y]

def error_sense(color):
    """
    color: реальный цвет, который находится под роботом
    return: искаженный цвет 
    """
    return 'r' if color == 'g' else 'g'

# p = [[0,0.5,0,0,0],
#      [0,0.3,0.2,0,0],
#      [0,0,0,0,0],
#      [0,0,0,0,0],
#      [0,0,0,0,0]]

p = []
for i in range(5):
    p.append([1/25 for j in range(5)])
        

world = [['g','r','r','g','g'],
         ['g','r','r','g','g'],
         ['g','g','g','g','g'],
         ['g','g','r','g','r'],
         ['r','r','r','r','g']]

Z = 'r'

p =  [[0,0,0,0,0],
      [0,0,0,0,0],
      [0,1,0,0,0],
      [0,0,0,0,0],
      [0,0,0,0,0]]


real_pos = [[0,0,0,0,0],
            [0,0,0,0,0],
            [0,1,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]]

moveset = [[1, 1], [1, 0], [1, -1], 
           [0, 1], [0, 0], [0, -1], 
           [-1, 1], [-1, 0], [-1, -1]]

u = [-1, -1]
# Тест функции движения
#print('\n', *move(p, u), sep='\n')
# Тест функции сенсеров
# for _ in range(5):
#     p = sense(p, Z)
#     print('\n', *p, sep='\n')
#print(*enumerate(p), sep='\n')
#print(argmax(p))

accuracy_sensor = 0.8

# Попытка симуляции
for _ in range(10):
    # Случайно выбираем направление движения
    u = random.choice(moveset)
    flag = random.random() < accuracy_sensor
    #ревльная позиция робота
    real_pos_buf = argmax(real_pos)
    # Тут должна быть попытка получить инфу с датчика 
    p = sense(p, world[real_pos_buf[1]][real_pos_buf[0]]) if flag else sense(p, error_sense(error_sense(world[real_pos_buf[1]][real_pos_buf[0]])))
    # Попытка понять где находимся на карте
    predict = argmax(p)
    real_pos[real_pos_buf[1]][real_pos_buf[0]] = 0

    # Куда-то двигаемся
    p = move(p, u)
    buf_random = random.random()
    if u[0] == 0 and u[1] == 0:
        continue
    # Определение реальная позиция робота
    if buf_random < 0.1:
        #Если двжемся по оси У 
        if u[0] == 0:
            real_pos[(real_pos_buf[1]-u[1]+1) % len(p)][(real_pos_buf[0]-u[0]) % len(p)] = 1
        #Если двжемся по оси Х
        if u[1] == 0:
            real_pos[(real_pos_buf[1]-u[1]) % len(p)][(real_pos_buf[0]-u[0]+1) % len(p)] = 1
        #Если двжемся по диагонали 
        if u[1] != 0 and u[0] != 0:
            real_pos[(real_pos_buf[1]-u[1]+1) % len(p)][(real_pos_buf[0]-u[0]+1) % len(p)] = 1
    elif buf_random >0.9:
        #Если двжемся по оси У 
        if u[0] == 0:
            real_pos[(real_pos_buf[1]-u[1]-1) % len(p)][(real_pos_buf[0]-u[0]) % len(p)] = 1
        #Если двжемся по оси Х
        if u[1] == 0:
            real_pos[(real_pos_buf[1]-u[1]) % len(p)][(real_pos_buf[0]-u[0]-1) % len(p)] = 1
        #Если двжемся по диагонали 
        if u[1] != 0 and u[0] != 0:
            real_pos[(real_pos_buf[1]-u[1]-1) % len(p)][(real_pos_buf[0]-u[0]-1) % len(p)] = 1
    else:
        real_pos[(real_pos_buf[1]-u[1]) % len(p)][(real_pos_buf[0]-u[0]) % len(p)] = 1

    print(p, sep='\n')
    print('------------------')
    print(real_pos, sep='\n')
