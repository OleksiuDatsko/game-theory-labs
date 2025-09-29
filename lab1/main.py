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
            print(num, end="\t",)
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
        print("Сідлові точки (індекси та значення):\n",  saddle_points, sep="")
    else:
        print("Сідлових точок немає.")

print("==== Приклад 1 ====")
matrix = [
    [ 5,  3, -1],
    [ 5,  5, -4],
    [ 3,  3,  1],
    [-4,  4,  4],
    [ 5,  3,  4]
]
analyze_game(matrix)

print("\n\n\n")
print("==== Приклад 2 ====")
matrix = [
    [ 5,  5,  2],
    [ 5,  4, -4],
    [ 5, -2,  1],
    [-4,  4,  0],
    [ 5,  4,  3]
]

analyze_game(matrix)

print("\n\n\n")
print("==== Приклад 3 ====")
matrix = [
    [ 2,  3,  4],
    [ 2,  3,  4],
    [ 3,  3,  4],
    [ 2,  3,  4],
    [ 2,  3,  4]
]

analyze_game(matrix)
