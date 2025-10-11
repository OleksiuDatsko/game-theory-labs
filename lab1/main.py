def analyze_game(matrix):
    m = len(matrix)
    n = len(matrix[0])

    # Мінімальні значення по рядках
    row_minima = [min(row) for row in matrix]
    # Максимальні значення по стовпцях
    col_maxima = [max(matrix[i][j] for i in range(m)) for j in range(n)]

    max_of_row_minima = max(row_minima)
    min_of_col_maxima = min(col_maxima)

    # Знаходження сідлових точок
    saddle_points = []
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == max_of_row_minima == min_of_col_maxima:
                saddle_points.append((i, j, matrix[i][j]))

    print("Конфліктна ситуація - ігрова матриця:")
    for row in matrix:
        for num in row:
            print(
                num,
                end="\t",
            )
        print()
    print("\nРезультати аналізу:")
    print("Мінімальні по рядках:", row_minima)
    print("Максимальні по стовпцях:", col_maxima)
    print("Max з мінімальних по рядках (нижня ціна):", max_of_row_minima)
    print("Min з максимальних по стовпцях (верхня ціна):", min_of_col_maxima)
    if max_of_row_minima == min_of_col_maxima:
        print("Ціни в сідлових точках:", max_of_row_minima)
    if saddle_points:
        print("Кількість сідлових точок:", len(saddle_points))
        print("Сідлові точки (індекси та значення):\n", saddle_points, sep="")
    else:
        print("Сідлових точок немає.")
    return saddle_points


matrices = {
    "Одна сідлова точка 1": [
        [1, 4, 5],
        [-4, 0, -1],
        [-3, -1, -3],
        [0, -2, 3],
        [-2, 2, 4],
    ],
    "Одна сідлова точка 2": [
        [3, 2, 5],
        [4, 0, 1],
        [1, -1, 4],
        [-3, 0, 3],
        [5, -1, -4],
    ],
    "Без сідлових точок 1": [
        [2, -4, 5],
        [-1, 4, 2],
        [1, -1, 4],
        [0, 5, 3],
        [-4, 0, 1],
    ],
    "Без сідлових точок 2": [
        [2, 2, -2],
        [-1, 1, 2],
        [1, -1, -3],
        [-2, 3, -4],
        [0, 4, 1],
    ],
    "Декілька сідлових точок": [
        [0, -1, 1],
        [2, 3, 4],
        [0, 4, 3],
        [2, 3, 2],
        [-3, 2, -3],
    ],
}


for key, value in matrices.items():
    print(f"\n\n\n==== {key} ====")
    analyze_game(value)
