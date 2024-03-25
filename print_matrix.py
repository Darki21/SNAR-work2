def print_matrix(matrix, rows, columns):
    """
    Печатает матрицу в удобном для чтения виде.

    :param matrix: матрица
    :param rows: кол-во строк матрицы
    :param columns: кол-во столбцов матрицы
    :return: None
    """

    for i in range(rows):
        for j in range(columns):
            print(matrix[i][j], end="; ")
        print("\n")
