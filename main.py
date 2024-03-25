import tkinter as tk
from tkinter import ttk

from random import random

from field_generate_start_probabilities import field_generate_start_probabilities
from field_generate_colour import field_generate_colour
from print_matrix import print_matrix

from generate_random_start_position import generate_random_start_position

from take_system_time import take_system_time

from sense_updated import sense
from move import move


# options
# change field size
def update_field_size_rows_up():
    """
    Увеличивает размер поля (высота).

    :param: None
    :return: None
    """
    y = int(stringvar_field_rows.get())
    # ограничение: до 12 клеток
    if y < 12:
        y += 1
    stringvar_field_rows.set(str(y))
    print("Новые размеры: ", stringvar_field_rows.get(), " на ", stringvar_field_columns.get())


def update_field_size_rows_down():
    """
    Уменьшает размер поля (высота).

    :param: None
    :return: None
    """
    y = int(stringvar_field_rows.get())
    # ограничение: не менее 2 клеток
    if y > 2:
        y -= 1
    stringvar_field_rows.set(str(y))
    print("Новые размеры: ", stringvar_field_rows.get(), " на ", stringvar_field_columns.get())


def update_field_size_y_columns():
    """
    Увеличивает размер поля (ширина).

    :param: None
    :return: None
    """
    x = int(stringvar_field_columns.get())
    # ограничение: до 12 клеток
    if x < 12:
        x += 1
    stringvar_field_columns.set(str(x))
    print("Новые размеры: ", stringvar_field_rows.get(), " на ", stringvar_field_columns.get())


def update_field_size_columns_down():
    """
    Уменьшает размер поля (ширина).

    :param: None
    :return: None
    """
    x = int(stringvar_field_columns.get())
    # ограничение: не менее 2 клеток
    if x > 2:
        x -= 1
    stringvar_field_columns.set(str(x))
    print("Новые размеры: ", stringvar_field_rows.get(), " на ", stringvar_field_columns.get())


# probability matrix
def generate_new_probability_matrix(x, y, p, tile_x, tile_y):
    """
    Отрисовывает матрицу вероятностей.

    :param x: размер поля (ширина)
    :param y: размер поля (высота)
    :param p: матрица распределения вероятностей
    :param tile_x: размер клетки матрицы (ширина)
    :param tile_y: размер клетки матрицы (высота)
    :return: None
    """

    tile_pos_x = 0
    tile_pos_y = 0
    for i in range(x):
        for j in range(y):
            # draw empty tile
            canvas_matrix.create_rectangle(tile_pos_x,
                                           tile_pos_y,
                                           tile_pos_x + tile_x,
                                           tile_pos_y + tile_y,
                                           fill="white", outline="black")
            # put probability
            canvas_matrix.create_text(tile_pos_x + tile_x // 2,
                                      tile_pos_y + tile_y // 2,
                                      text=p[i][j],
                                      tags="txt")

            tile_pos_x += tile_x
        tile_pos_x = 0
        tile_pos_y += tile_y


# world map
def generate_new_world_map(x, y, c, tile_x, tile_y):
    """
    Отрисовывает карту мира.

    :param x: размер поля (ширина)
    :param y: размер поля (высота)
    :param c: карта распределения цвета
    :param tile_x: размер клетки поля (ширина)
    :param tile_y: размер клетки поля (высота)
    :return: None
    """

    tile_pos_x = 0
    tile_pos_y = 0
    for i in range(x):
        for j in range(y):
            # select colour
            if c[i][j] == 'r':
                tile_colour = "red"
            else:
                tile_colour = "green"

            # draw tile
            canvas_world.create_rectangle(tile_pos_x,
                                          tile_pos_y,
                                          tile_pos_x + tile_x,
                                          tile_pos_y + tile_y,
                                          fill=tile_colour,
                                          outline="black",
                                          tags="world_map")

            tile_pos_x += tile_x
        tile_pos_x = 0
        tile_pos_y += tile_y


# robot position
def put_robot_in_the_world(pos, tile_x, tile_y):
    """
    Рисует, где находится робот.

    :param pos: местоположение робота (x-индекс и y-индекс клетки)
    :param tile_x: размер клетки поля (ширина)
    :param tile_y: размер клетки поля (высота)
    :return:
    """
    canvas_world.create_oval(pos[0] * tile_x,
                             pos[1] * tile_y,
                             pos[0] * tile_x + tile_x,
                             pos[1] * tile_y + tile_y,
                             outline='black',
                             width=3,
                             tags="robot")


# refresh content
def refresh(tile_x, tile_y):
    """
    Вызывает функции для обновления карты мира, положения робота на новой карте и матрицы распределения вероятностей.

    :param tile_x: размер клетки (ширина)
    :param tile_y: размер клетки (высота)
    :return: None
    """

    global colour_map
    global probability
    global position

    print("ОБНОВЛЕНИЕ ПОЛЯ")
    x = int(stringvar_field_rows.get())
    y = int(stringvar_field_columns.get())
    # start position (x, y) (indexes of the tile)
    position = generate_random_start_position(y, x)
    print("Где заспавнился робот: ", position[0], ";", position[1])
    # probability matrix
    probability = field_generate_start_probabilities(x, y)
    print("Новая сгенерированная матрица: ")
    print_matrix(probability, x, y)
    # colour map
    colour_map = field_generate_colour(x, y)
    print("Новая цветовая карта: ")
    print_matrix(colour_map, x, y)

    canvas_world.delete("all")
    generate_new_world_map(x, y, colour_map, tile_x, tile_y)
    put_robot_in_the_world(position, tile_x, tile_y)

    message = take_system_time()
    message += ' '
    message += event_cases["init"]
    stringvar_events.set(message)

    canvas_matrix.delete("all")
    generate_new_probability_matrix(x, y, probability, tile_x, tile_y)


# sensors
def refresh_sense_data():
    """
    Получает информацию от сенсора.

    :return: None
    """

    global probability

    # учитывается то, что может быть успех, а может быть и нет
    # шансы те же, что в sense
    # успех
    pHit = 0.6
    # ложные срабатывания
    pMiss = 0.2

    sense_chance = random()
    # NB сначала выбирается СТРОКА, потом ЭЛЕМЕНТ В СТРОКЕ
    sensor_measurement = colour_map[position[1]][position[0]]

    # в зависимости от шанса решаем, датчик нам показал правду (не меняем sensor_measurement) или соврал
    # (меняем sensor_measurement на противоположное)
    if sense_chance > pHit:
        if sensor_measurement == 'r':
            sensor_measurement = 'g'
        else:
            sensor_measurement = 'r'

    if sensor_measurement == 'r':
        message = take_system_time()
        message += ' '
        message += event_cases["sense_red"]
        stringvar_events.set(message)
    else:
        message = take_system_time()
        message += ' '
        message += event_cases["sense_green"]
        stringvar_events.set(message)
    print("Зритель видит, что робот стоит на клетке с индексами: ", position[0], "; ", position[1])
    print("Показание датчика: ", sensor_measurement)
    # пересчёт матрицы распределения вероятностей
    probability = sense(probability, sensor_measurement, colour_map)
    print("Обновлённая матрица распределения вероятностей:")
    print(probability)
    generate_new_probability_matrix(int(stringvar_field_rows.get()), int(stringvar_field_columns.get()), probability,
                                    tile_size_x, tile_size_y)
    root.after(4000, refresh_sense_data)


# movement
def step_up():
    """
    Принимает управляющее воздействие со стороны пользователя (робот идёт вверх).

    :return:
    """

    global probability
    global position

    canvas_world.delete("robot")
    canvas_matrix.delete("all")

    # учёт того, что может быть либо успех, либо неуспех; 2 случая неуспеха: оставлись на месте, переместились на 2
    # шансы те же что в функции move
    pExact = 0.8
    # pOvershoot = 0.1
    # pUndershoot = 0.1

    # шанс -- это не получка и не аванс
    movement_chance = random()

    # успех
    if movement_chance < pExact:
        u = shift_cases["up"]
        position[0] += u[0]
        position[1] += u[1]

        if position[1] < 0:
            position[1] = int(stringvar_field_rows.get()) - 1

        message = take_system_time()
        message += ' '
        message += event_cases["move_up_success"]
        stringvar_events.set(message)

    # NB тут проблема в том, что это покрытие частного случая,
    # а как это сделать так, чтобы под общий случай подходило?
    # неуспех
    # надо выбрать, какой из двух неуспехов
    # два варианта неуспеха равновероятны между собой, поэтом сравнение идёт с 0.5
    else:

        movement_chance = random()

        # остались на месте
        if movement_chance >= 0.5:
            # не перемещаемся
            u = shift_cases["none"]
            message = take_system_time()
            message += ' '
            message += event_cases["move_up_fail_undershoot"]
            stringvar_events.set(message)

        # сместились на две клетки
        else:
            u = shift_cases["up"]
            position[0] += u[0]
            position[1] += u[1]

            if position[1] < 0:
                position[1] = int(stringvar_field_rows.get()) - 1

            u = shift_cases["up"]
            position[0] += u[0]
            position[1] += u[1]

            if position[1] < 0:
                position[1] = int(stringvar_field_rows.get()) - 1

            message = take_system_time()
            message += ' '
            message += event_cases["move_up_fail_overshoot"]
            stringvar_events.set(message)

    probability = move(probability, u)

    put_robot_in_the_world(position, tile_size_x, tile_size_y)
    generate_new_probability_matrix(int(stringvar_field_rows.get()), int(stringvar_field_columns.get()),
                                    probability, tile_size_x, tile_size_y)

    print("Зритель видит, что робот встал на позицию ", position[0], ";", position[1])
    print("Обновлённая матрица вероятностей: ")
    print(probability)


def step_down():
    """
    Принимает управляющее воздействие со стороны пользователя (робот идёт вниз).

    :return:
    """

    global probability
    global position

    canvas_world.delete("robot")
    canvas_matrix.delete("all")

    pExact = 0.8
    movement_chance = random()

    # успех
    if movement_chance < pExact:
        u = shift_cases["down"]
        position[0] += u[0]
        position[1] += u[1]

        # пересчёт, если вышли за границу
        if position[1] == int(stringvar_field_rows.get()):
            position[1] = 0

        message = take_system_time()
        message += ' '
        message += event_cases["move_down_success"]
        stringvar_events.set(message)

    # неуспех
    else:
        movement_chance = random()

        # остались на месте
        if movement_chance <= 0.5:
            # не перемещаемся
            u = shift_cases["none"]
            message = take_system_time()
            message += ' '
            message += event_cases["move_down_fail_undershoot"]
            stringvar_events.set(message)

        # сместились на две клетки
        else:
            u = shift_cases["down"]
            position[0] += u[0]
            position[1] += u[1]

            # пересчёт, если вышли за границу
            if position[1] == int(stringvar_field_rows.get()):
                position[1] = 0

            u = shift_cases["down"]
            position[0] += u[0]
            position[1] += u[1]

            # пересчёт, если вышли за границу
            if position[1] == int(stringvar_field_rows.get()):
                position[1] = 0

            message = take_system_time()
            message += ' '
            message += event_cases["move_down_fail_overshoot"]
            stringvar_events.set(message)

    probability = move(probability, u)

    put_robot_in_the_world(position, tile_size_x, tile_size_y)
    generate_new_probability_matrix(int(stringvar_field_rows.get()), int(stringvar_field_columns.get()),
                                    probability, tile_size_x, tile_size_y)

    print("Зритель видит, что робот встал на позицию ", position[0], ";", position[1])
    print("Обновлённая матрица вероятностей: ")
    print(probability)


def step_left():
    """
    Принимает управляющее воздействие со стороны пользователя (робот идёт влево).

    :return:
    """

    global probability
    global position

    canvas_world.delete("robot")
    canvas_matrix.delete("all")

    pExact = 0.8
    movement_chance = random()

    # успех
    if movement_chance < pExact:

        u = shift_cases["left"]
        position[0] += u[0]
        position[1] += u[1]

        # пересчёт, если вышли за границу
        if position[0] < 0:
            position[0] = int(stringvar_field_columns.get()) - 1

        message = take_system_time()
        message += ' '
        message += event_cases["move_left_success"]
        stringvar_events.set(message)

    # неуспех
    else:
        movement_chance = random()

        # остались на месте
        if movement_chance <= 0.5:
            # не перемещаемся
            u = shift_cases["none"]
            message = take_system_time()
            message += ' '
            message += event_cases["move_left_fail_undershoot"]
            stringvar_events.set(message)

        # сместились на две клетки
        else:

            u = shift_cases["left"]
            position[0] += u[0]
            position[1] += u[1]

            # пересчёт, если вышли за границу
            if position[0] < 0:
                position[0] = int(stringvar_field_columns.get()) - 1

            u = shift_cases["left"]
            position[0] += u[0]
            position[1] += u[1]

            # пересчёт, если вышли за границу
            if position[0] < 0:
                position[0] = int(stringvar_field_columns.get()) - 1

            message = take_system_time()
            message += ' '
            message += event_cases["move_left_fail_overshoot"]
            stringvar_events.set(message)

    probability = move(probability, u)

    put_robot_in_the_world(position, tile_size_x, tile_size_y)
    generate_new_probability_matrix(int(stringvar_field_rows.get()), int(stringvar_field_columns.get()),
                                    probability, tile_size_x, tile_size_y)

    print("Зритель видит, что робот встал на позицию ", position[0], ";", position[1])
    print("Обновлённая матрица вероятностей: ")
    print(probability)


def step_right():
    """
    Принимает управляющее воздействие со стороны пользователя (робот идёт вправо).

    :return:
    """

    global probability
    global position

    canvas_world.delete("robot")
    canvas_matrix.delete("all")

    pExact = 0.8
    movement_chance = random()

    # успех
    if movement_chance < pExact:

        u = shift_cases["right"]
        position[0] += u[0]
        position[1] += u[1]

        # пересчёт, если вышли за границу
        if position[0] == int(stringvar_field_columns.get()):
            position[0] = 0

        message = take_system_time()
        message += ' '
        message += event_cases["move_right_success"]
        stringvar_events.set(message)

    # неуспех
    else:
        movement_chance = random()

        # остались на месте
        if movement_chance <= 0.5:
            # не перемещаемся
            u = shift_cases["none"]
            message = take_system_time()
            message += ' '
            message += event_cases["move_right_fail_undershoot"]
            stringvar_events.set(message)

        # сместились на две клетки
        else:

            u = shift_cases["right"]
            position[0] += u[0]
            position[1] += u[1]

            # пересчёт, если вышли за границу
            if position[0] == int(stringvar_field_columns.get()):
                position[0] = 0

            u = shift_cases["right"]
            position[0] += u[0]
            position[1] += u[1]

            # пересчёт, если вышли за границу
            if position[0] == int(stringvar_field_columns.get()):
                position[0] = 0

            message = take_system_time()
            message += ' '
            message += event_cases["move_right_fail_overshoot"]
            stringvar_events.set(message)

    probability = move(probability, u)

    put_robot_in_the_world(position, tile_size_x, tile_size_y)
    generate_new_probability_matrix(int(stringvar_field_rows.get()), int(stringvar_field_columns.get()),
                                    probability, tile_size_x, tile_size_y)

    print("Зритель видит, что робот встал на позицию ", position[0], ";", position[1])
    print("Обновлённая матрица вероятностей: ")
    print(probability)


# possible events
event_cases = {"init": "Симуляция запущена. Локация обновлена. Робот появился в случайном месте.",
               "sense_red": "Опрос датчика. Робот считает, что он на красной клетке.",
               "sense_green": "Опрос датчика. Робот считает, что он на зелёной клетке.",

               "move_up_success": "Следующий шаг траектории -- вверх. Успех",
               "move_up_fail_undershoot": "Следующий шаг траектории -- вверх. Неудача. Робот на месте.",
               "move_up_fail_overshoot": "Следующий шаг траектории -- вверх. Неудача. Лишний шаг.",

               "move_down_success": "Следующий шаг траектории -- вниз. Успех",
               "move_down_fail_undershoot": "Следующий шаг траектории -- вниз. Неудача. Робот на месте.",
               "move_down_fail_overshoot": "Следующий шаг траектории -- вниз. Неудача. Лишний шаг.",

               "move_right_success": "Следующий шаг траектории -- вправо. Успех",
               "move_right_fail_undershoot": "Следующий шаг траектории -- вправо. Неудача. Робот на месте.",
               "move_right_fail_overshoot": "Следующий шаг траектории -- вправо. Неудача. Лишний шаг.",

               "move_left_success": "Следующий шаг траектории -- влево. Успех",
               "move_left_fail_undershoot": "Следующий шаг траектории -- влево. Неудача. Робот на месте.",
               "move_left_fail_overshoot": "Следующий шаг траектории -- влево. Неудача. Лишний шаг."
               }
# shift cases
shift_cases = {"up": [0, -1],
               "down": [0, 1],
               "left": [-1, 0],
               "right": [1, 0],
               "none": [0, 0]}
# create field
# size
field_rows = 12
field_columns = 12
# tile size
tile_size_x = 50
tile_size_y = 50
# start position (x, y) (indexes of the tile)
position = generate_random_start_position(field_columns, field_rows)
print("Где заспавнился робот: ", position[0], ";", position[1])
# probability matrix
probability = field_generate_start_probabilities(field_rows, field_columns)
print("Сгенерированная матрица: ")
print_matrix(probability, field_rows, field_columns)
# colour map
colour_map = field_generate_colour(field_rows, field_columns)
print("Цветовая карта: ")
print_matrix(colour_map, field_rows, field_columns)

# create main window
root = tk.Tk()
root.title("Главное окно")

# create main frames
frame_options = ttk.Labelframe(root,
                               text="Опции",
                               relief=tk.SOLID)
frame_matrix = ttk.LabelFrame(root,
                              text="Матрица распределени вероятностей",
                              relief=tk.SOLID)
frame_world = ttk.LabelFrame(root,
                             text="Карта мира",
                             relief=tk.SOLID)
frame_controls = ttk.LabelFrame(root,
                                text="Управление роботом",
                                relief=tk.SOLID)
frame_events_messages = ttk.LabelFrame(root,
                                       text="События",
                                       relief=tk.SOLID)

# options
stringvar_field_rows = tk.StringVar(value=str(field_rows))
stringvar_field_columns = tk.StringVar(value=str(field_columns))

frame_set_size = ttk.LabelFrame(frame_options,
                                text="Задать размер поля",
                                relief=tk.SOLID)
button_up_rows = tk.Button(frame_set_size,
                           text="/\\",
                           command=update_field_size_rows_up)
button_down_rows = tk.Button(frame_set_size,
                             text="\/",
                             command=update_field_size_rows_down)

label_y_size = tk.Label(frame_set_size,
                        textvariable=stringvar_field_rows)
label_x = tk.Label(frame_set_size,
                   text=" x ")

button_up_columns = tk.Button(frame_set_size,
                              text="/\\",
                              command=update_field_size_y_columns)
button_down_columns = tk.Button(frame_set_size,
                                text="\/",
                                command=update_field_size_columns_down)
label_x_size = tk.Label(frame_set_size,
                        textvariable=stringvar_field_columns)

button_confirm = tk.Button(frame_set_size,
                           text="Обновить симуляцию",
                           command=lambda tile_x=tile_size_x,
                                          tile_y=tile_size_y: refresh(tile_x, tile_y))

button_up_rows.grid(row=0, column=0)
button_down_rows.grid(row=2, column=0)
label_y_size.grid(row=1, column=0)

label_x.grid(row=1, column=2)

button_up_columns.grid(row=0, column=3)
button_down_columns.grid(row=2, column=3)
label_x_size.grid(row=1, column=3)

button_confirm.grid(row=3, column=2)

frame_set_size.grid(row=0, column=0)

# probability matrix
canvas_matrix = tk.Canvas(frame_matrix, width=field_rows * tile_size_x, height=field_columns * tile_size_y)
canvas_matrix.pack()
# initial matrix
generate_new_probability_matrix(field_rows, field_columns, probability, tile_size_x, tile_size_y)

# world map
canvas_world = tk.Canvas(frame_world, width=field_rows * tile_size_x, height=field_columns * tile_size_y)
canvas_world.pack()
# initial world map
generate_new_world_map(field_rows, field_columns, colour_map, tile_size_x, tile_size_y)

# initial robot position
put_robot_in_the_world(position, tile_size_x, tile_size_y)

# controls
button_up = tk.Button(frame_controls,
                      text="/\\",
                      command=step_up)
button_down = tk.Button(frame_controls,
                        text="\/",
                        command=step_down)
button_left = tk.Button(frame_controls,
                        text="<",
                        command=step_left)
button_right = tk.Button(frame_controls,
                         text=">",
                         command=step_right)

button_up.grid(row=0, column=1)
button_down.grid(row=2, column=1)
button_left.grid(row=1, column=0)
button_right.grid(row=1, column=2)

# messages
stringvar_events = tk.StringVar(value=event_cases["init"])
label_events = tk.Label(frame_events_messages,
                        textvariable=stringvar_events)
label_events.grid(row=0, column=0)

# place frames
frame_options.grid(row=1, column=0)
frame_matrix.grid(row=0, column=0)
frame_world.grid(row=0, column=1)
frame_controls.grid(row=1, column=1)
frame_events_messages.grid(row=2, column=0)

refresh_sense_data()
root.mainloop()
