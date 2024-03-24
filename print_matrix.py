def print_matrix(matrix, x, y):
    """
    Печатает матрицу в удобном для чтения виде.

    :param matrix: матрица
    :param x: кол-во строк матрицы
    :param y: кол-во столбцов матрицы
    :return: None
    """

    for i in range(x):
        for j in range(y):
            print(matrix[i][j], end="; ")
        print("\n")
