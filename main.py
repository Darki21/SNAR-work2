import tkinter as tk
from tkinter import ttk

from field_generate_colour import field_generate_colour
from field_generate_start_probabilities import field_generate_start_probabilities

from move import move
from sense_updated import sense


# настройки
def settings():
    """
    Создаёт окно настроек симуляции.

    :param: None
    :return: None
    """

    global is_config_being_redacted

    # закрытие окна настроек
    def settings_close():
        """
        Закрывает окно настроек.

        :param: None
        :return: None
        """

        global is_config_being_redacted

        stringvar_status.set(status_list[2])
        window_settings.destroy()
        is_config_being_redacted = False

    is_config_being_redacted = True
    window_settings = tk.Toplevel(root)
    window_settings.title("Настройкий")
    frame_set_size = ttk.LabelFrame(window_settings,
                                    text="Задать размер поля",
                                    relief=tk.SOLID)
    button_up_x = tk.Button(frame_set_size,
                            text="/\\",
                            command=update_field_size_x_up)
    button_down_x = tk.Button(frame_set_size,
                              text="\/",
                              command=update_field_size_x_down)

    label_x_size = tk.Label(frame_set_size,
                            textvariable=stringvar_x_size)
    label_x = tk.Label(frame_set_size,
                       text=" x ")

    button_up_y = tk.Button(frame_set_size,
                            text="/\\",
                            command=update_field_size_y_up)
    button_down_y = tk.Button(frame_set_size,
                              text="\/",
                              command=update_field_size_y_down)
    label_y_size = tk.Label(frame_set_size,
                            textvariable=stringvar_y_size)

    button_confirm = tk.Button(frame_set_size,
                               text="Подтвердить изменения",
                               command=settings_close)

    button_up_x.grid(row=0, column=0)
    button_down_x.grid(row=2, column=0)
    label_x_size.grid(row=1, column=0)

    label_x.grid(row=1, column=2)

    button_up_y.grid(row=0, column=3)
    button_down_y.grid(row=2, column=3)
    label_y_size.grid(row=1, column=3)

    button_confirm.grid(row=3, column=2)

    frame_set_size.grid(row=0, column=0)


# обновление размеров поля
def update_field_size_x_up():
    """
    Принимает изменения размера поля со стороны пользователя.

    :param: None
    :return: None
    """
    global field_x
    # ограничение: до 12 клеток
    if field_x < 12:
        field_x += 1
    stringvar_x_size.set(field_x)


def update_field_size_x_down():
    """
    Принимает изменения размера поля со стороны пользователя.

    :param: None
    :return: None
    """
    global field_x
    # ограничение: не менее 2 клеток
    if field_x > 2:
        field_x -= 1
    stringvar_x_size.set(field_x)


def update_field_size_y_up():
    """
    Принимает изменения размера поля со стороны пользователя.

    :param: None
    :return: None
    """
    global field_y
    # ограничение: до 12 клеток
    if field_y < 12:
        field_y += 1
    stringvar_y_size.set(field_y)


def update_field_size_y_down():
    """
    Принимает изменения размера поля со стороны пользователя.

    :param: None
    :return: None
    """
    global field_y
    # ограничение: не менее 2 клеток
    if field_y > 2:
        field_y -= 1
    stringvar_y_size.set(field_y)


# обновление поля
def simulation_generate():
    """
    Отрисовывает поле с цветными клетками.

    :return:
    """

    global colour_map
    global p

    canvas_world.delete("all")
    canvas_matrix.delete("all")

    canvas_world.config(width=field_x * tile_size_x, height=field_y * tile_size_y)
    canvas_matrix.config(width=field_x * tile_size_x, height=field_y * tile_size_y)

    colour_map = field_generate_colour(field_x, field_y)
    p = field_generate_start_probabilities(field_x, field_y)

    # ДЛЯ ПРОВЕРОК
    print("Поле сгенерировано")
    print("Цветовое распределение: ")
    print(colour_map)
    print("Распределение вероятностей: ")
    for i in range(field_x):
        for j in range(field_y):
            print(p[i][j], sep='; ')
        print('\n')

    # draw colour tiles
    tile_pos_x = 0
    tile_pos_y = 0

    for i in range(field_x):
        for j in range(field_y):

            # select colour
            if colour_map[i][j] == 'g':
                tile_colour = 'green'
            else:
                tile_colour = 'red'

            # draw 1 tile
            canvas_world.create_rectangle(tile_pos_x,
                                          tile_pos_y,
                                          tile_pos_x + tile_size_x,
                                          tile_pos_y + tile_size_y,
                                          fill=tile_colour, outline="black")

            tile_pos_x += tile_size_x
        tile_pos_x = 0
        tile_pos_y += tile_size_y

    # draw matrix
    tile_pos_x = 0
    tile_pos_y = 0
    for i in range(field_x):
        for j in range(field_y):
            # draw empty tile
            tile_tag = str(i)
            tile_tag += str(j)
            canvas_matrix.create_rectangle(tile_pos_x,
                                           tile_pos_y,
                                           tile_pos_x + tile_size_x,
                                           tile_pos_y + tile_size_y,
                                           fill="white", outline="black")
            # put probability
            canvas_matrix.create_text(tile_pos_x + tile_size_x // 2,
                                      tile_pos_y + tile_size_y // 2,
                                      text=p[i][j],
                                      tag="txt")

            tile_pos_x += tile_size_x
        tile_pos_x = 0
        tile_pos_y += tile_size_y

    # заспавнить робота
    canvas_world.create_oval(pos[0] * tile_size_x,
                             pos[1] * tile_size_y,
                             pos[0] * tile_size_x + tile_size_x,
                             pos[1] * tile_size_y + tile_size_y,
                             outline='black',
                             width=3,
                             tag="robot")


# перемещения
def step_up():
    """
    Принимает управляющее воздействие от пользователя и меняет переменную, содержащую направление шага робота.
    Вызывает функцию move для пересчёта матрицы распределения вероятностей, отрисовывает новую позицию робота
    (цикличность мира учитывается), отрисовывает новую матрицу распределения.

    :return: None
    """

    global U
    global p
    global pos
    global should_go_through_border_up_to_down

    U[1] = -1
    print("Пользователь нажал кнопку вверх. Смещение U = ", U)
    pos[1] += U[1]
    # учитываем цикличность мира
    if pos[1] < 0:
        pos[1] = field_y - 1
        should_go_through_border_up_to_down = True
    p = move(p, U)
    refresh_robot_position()
    U = [0, 0]

    # ДЛЯ ПРОВЕРОК

    print("Новая позиция робота (индексы клеток) [x, y] = ", pos)
    print("Новая матрица распределения вероятностей: ", p)


def step_down():
    """
    Принимает управляющее воздействие от пользователя и меняет переменную, содержащую направление шага робота.
    Вызывает функцию move для пересчёта матрицы распределения вероятностей, отрисовывает новую позицию робота
    (цикличность мира учитывается), отрисовывает новую матрицу распределения.

    :return: None
    """

    global U
    global p
    global pos
    global should_go_through_border_down_to_up

    U[1] = 1
    print("Пользователь нажал кнопку вниз. Смещение U = ", U)
    pos[1] += U[1]
    # учитываем цикличность мира
    if pos[1] == field_y:
        pos[1] = 0
        should_go_through_border_down_to_up = True
    p = move(p, U)
    refresh_robot_position()
    U = [0, 0]

    # ДЛЯ ПРОВЕРОК

    print("Новая позиция робота (индексы клеток) [x, y] = ", pos)
    print("Новая матрица распределения вероятностей: ", p)


def step_left():
    """
    Принимает управляющее воздействие от пользователя и меняет переменную, содержащую направление шага робота.
    Вызывает функцию move для пересчёта матрицы распределения вероятностей, отрисовывает новую позицию робота
    (цикличность мира учитывается), отрисовывает новую матрицу распределения.

    :return: None
    """

    global U
    global p
    global pos
    global should_go_through_border_left_to_right

    U[0] = -1
    print("Пользователь нажал кнопку влево. Смещение U = ", U)
    pos[0] += U[0]
    # учитываем цикличность мира
    if pos[0] < 0:
        pos[0] = field_x - 1
        should_go_through_border_left_to_right = True
    p = move(p, U)
    refresh_robot_position()
    U = [0, 0]

    # ДЛЯ ПРОВЕРОК

    print("Новая позиция робота (индексы клеток) [x, y] = ", pos)
    print("Новая матрица распределения вероятностей: ", p)


def step_right():
    """
    Принимает управляющее воздействие от пользователя и меняет переменную, содержащую направление шага робота.
    Вызывает функцию move для пересчёта матрицы распределения вероятностей, отрисовывает новую позицию робота
    (цикличность мира учитывается), отрисовывает новую матрицу распределения.

    :return: None
    """

    global U
    global p
    global pos
    global should_go_through_border_right_to_left

    U[0] = 1
    print("Пользователь нажал кнопку вверх. Смещение U = ", U)
    pos[0] += U[0]
    # учитываем цикличность мира
    if pos[0] == field_x:
        pos[0] = 0
        should_go_through_border_right_to_left = True
    p = move(p, U)
    refresh_robot_position()
    U = [0, 0]

    # ДЛЯ ПРОВЕРОК

    print("Новая позиция робота (индексы клеток) [x, y] = ", pos)
    print("Новая матрица распределения вероятностей: ", p)


# отрисовка положения робота
# происходит после того, как пользователь тыкнул на стрелочку
def refresh_robot_position():
    """
    На основе смещения U вычисляет новое положение робота

    :return:
    """

    global should_go_through_border_left_to_right
    global should_go_through_border_right_to_left
    global should_go_through_border_up_to_down
    global should_go_through_border_down_to_up

    # NB pos была уже вычислена в предыдущих функциях
    # крайние случаи
    # левая граница, идём влево, должны оказаться в правой границе
    if should_go_through_border_left_to_right:
        canvas_world.move("robot", (field_x - 1)*tile_size_x, 0)
        should_go_through_border_left_to_right = False

    # правая граница, идём вправо, должны оказаться в левой границе
    elif should_go_through_border_right_to_left:
        canvas_world.move("robot", -(field_x - 1) * tile_size_x, 0)
        should_go_through_border_right_to_left = False

    # верхняя граница, идём вверх, должны оказаться в нижней границе
    elif should_go_through_border_up_to_down:
        canvas_world.move("robot", 0, (field_y - 1) * tile_size_y)
        should_go_through_border_up_to_down = False

    # нижняя граница, идём вних, должны оказаться в верхней границе
    elif should_go_through_border_down_to_up:
        canvas_world.move("robot", 0, -(field_y - 1) * tile_size_y)
        should_go_through_border_down_to_up = False

    # общий случай
    else:
        canvas_world.move("robot", U[0]*tile_size_x, U[1]*tile_size_y)


# отрисовка СОДЕРЖИМОГО матрицы распределения
def refresh_probability_matrix():
    """

    :return: None
    """
    if not is_config_being_redacted:
        canvas_matrix.delete("txt")
        tile_pos_x = 0
        tile_pos_y = 0
        for i in range(field_x):
            for j in range(field_y):
                # put probability
                canvas_matrix.create_text(tile_pos_x + tile_size_x // 2,
                                          tile_pos_y + tile_size_y // 2,
                                          text=p[i][j],
                                          tag="txt")

                tile_pos_x += tile_size_x
            tile_pos_x = 0
            tile_pos_y += tile_size_y


# NB Почему-то создание новой симуляции с ДРУГИМ размером всё ломает, функция перестаёт вызываться; отчего?
# опрос датчика и вызов sense для пересчёта матрицы распределения вероятностей
def get_sense():
    """

    :return:
    """

    global p

    Z = colour_map[pos[0]][pos[1]]
    print("Показание датчика: ", Z)
    p = sense(p, Z, colour_map)


# периодическеи вызывает сама себя, чтобы обновлять содержимое (где стоит робот и что в матрице распределения)
def refresh_screen():
    get_sense()
    refresh_probability_matrix()
    root.after(1000, refresh_screen)


# значения по умолчанию
# размер клетки
tile_size_x = 50
tile_size_y = 50
# размер поля
field_x = 4
field_y = 4
# распределение вероятностей
p = [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]
# распределение цветов
colour_map = field_generate_colour(field_x, field_y)
# положение робота [x, y] по индексам
pos = [0, 0]
# смещение робота
U = [0, 0]

# прочее
# сообщения для главного окна
status_list = ["всё хорошо",
               "для обновление рабочей области закройте текущее окно рабочей области",
               "настройки запуска симуляции были успешно обновлены"]
# флаги
# блокировка обновления поля, когда в настройках сидим (в целом, оно чинится запуском новой симуляции, но тем не менее)
# теперь ошибки выскакиывают только один раз
is_config_being_redacted = False
# border between dreams and reality
# нужен для "крайних" случаев, чтобы из одной границы робот перешёл в другую, а не ушёл бы в пустоту
should_go_through_border_left_to_right = False
should_go_through_border_right_to_left = False
should_go_through_border_down_to_up = False
should_go_through_border_up_to_down = False

# создание окна
root = tk.Tk()
root.title("Главное окно")

stringvar_y_size = tk.StringVar(value=field_y)
stringvar_x_size = tk.StringVar(value=field_x)
stringvar_status = tk.StringVar(value=status_list[0])

# конфигурация
frame_menu_window = ttk.Labelframe(root,
                                   text="Опции",
                                   relief=tk.SOLID)
button_simulation = tk.Button(frame_menu_window,
                              text="Запустить новую симуляцию",
                              command=simulation_generate)
button_settings = tk.Button(frame_menu_window,
                            text="Открыть окно настроек",
                            command=settings)
label_status = tk.Label(frame_menu_window,
                        textvariable=stringvar_status)

button_settings.grid(row=0, column=0)
button_simulation.grid(row=1, column=0)
label_status.grid(row=2, column=0)

# матрица распределения вероятностей
frame_matrix = ttk.LabelFrame(root,
                              text="Матрица распределени вероятностей",
                              relief=tk.SOLID)

canvas_matrix = tk.Canvas(frame_matrix, width=field_x * tile_size_x, height=field_y * tile_size_y)
canvas_matrix.pack()

# поле с роботом
frame_world = ttk.LabelFrame(root,
                             text="Карта мира",
                             relief=tk.SOLID)
canvas_world = tk.Canvas(frame_world, width=field_x * tile_size_x, height=field_y * tile_size_y)
canvas_world.pack()

simulation_generate()

# панель управления движениями
frame_controls = ttk.LabelFrame(root,
                                text="Управление роботом",
                                relief=tk.SOLID)
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

# размещение фреймов
frame_menu_window.grid(row=0, column=0)
frame_matrix.grid(row=0, column=1)
frame_world.grid(row=0, column=2)
frame_controls.grid(row=0, column=3)

refresh_screen()
root.mainloop()
