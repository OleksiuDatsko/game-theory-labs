import itertools
import csv

# --- КОНФІГУРАЦІЯ ---
BLUE_UNITS = 3
RED_UNITS = 6
ROADS = 3

PAYOFF_BLUE_WIN = (1, -2)
PAYOFF_BLUE_LOSE = (-1, 1)


def generate_strategies(units, roads):
    """Генерує всі можливі розподіли рот."""
    all_combinations = itertools.product(range(units + 1), repeat=roads)
    valid_strategies = [s for s in all_combinations if sum(s) == units]
    return valid_strategies


def calculate_payoff(blue_strat, red_strat):
    """Визначає виграш за правилами гри."""
    blue_wins = False
    for b, r in zip(blue_strat, red_strat):
        if b > r:
            blue_wins = True
            break

    if blue_wins:
        return PAYOFF_BLUE_WIN
    else:
        return PAYOFF_BLUE_LOSE


def save_matrix_to_csv(filename, matrix, blue_strategies, red_strategies):
    """Зберігає матрицю гри у CSV файл."""
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            header = ["С/Ч"] + [str(s) for s in red_strategies]
            writer.writerow(header)

            for i, blue_strat in enumerate(blue_strategies):
                row = [str(blue_strat)] 
                for j in range(len(red_strategies)):
                    row.append(str(matrix[i][j]))
                writer.writerow(row)

        print(f"\n[INFO] Матрицю успішно збережено у файл: {filename}")
    except Exception as e:
        print(f"\n[ERROR] Помилка при збереженні файлу: {e}")


def solve_game():
    print(f"--- ЛАБОРАТОРНА РОБОТА №6 (ВАРІАНТ 8) ---")

    # 1. Генерація стратегій
    blue_strategies = generate_strategies(BLUE_UNITS, ROADS)
    red_strategies = generate_strategies(RED_UNITS, ROADS)

    n_blue = len(blue_strategies)
    n_red = len(red_strategies)

    matrix = [[(0, 0) for _ in range(n_red)] for _ in range(n_blue)]

    for i in range(n_blue):
        for j in range(n_red):
            matrix[i][j] = calculate_payoff(blue_strategies[i], red_strategies[j])

    save_matrix_to_csv("game_matrix_var8.csv", matrix, blue_strategies, red_strategies)

    # 3. Пошук Рівноваги Неша
    nash_equilibria = []
    for i in range(n_blue):
        for j in range(n_red):
            current_payoff_blue = matrix[i][j][0]
            current_payoff_red = matrix[i][j][1]

            blue_can_improve = False
            for k in range(n_blue):
                if matrix[k][j][0] > current_payoff_blue:
                    blue_can_improve = True
                    break

            red_can_improve = False
            for k in range(n_red):
                if matrix[i][k][1] > current_payoff_red:
                    red_can_improve = True
                    break

            if not blue_can_improve and not red_can_improve:
                nash_equilibria.append(((i, j), matrix[i][j]))

    print("\n1. РІВНОВАГА НЕША (НЕКООПЕРАТИВНА):")
    if not nash_equilibria:
        print("  У чистих стратегіях рівноваги Неша немає.")
    else:
        for (i, j), payoff in nash_equilibria:
            print(
                f"  Сині: {blue_strategies[i]}, Червоні: {red_strategies[j]} -> Виграш: {payoff}"
            )

    # 4. Оптимум за Парето
    pareto_points = []
    for i in range(n_blue):
        for j in range(n_red):
            current_b, current_r = matrix[i][j]
            is_dominated = False

            for k in range(n_blue):
                for l in range(n_red):
                    other_b, other_r = matrix[k][l]
                    if (other_b >= current_b and other_r >= current_r) and (
                        other_b > current_b or other_r > current_r
                    ):
                        is_dominated = True
                        break
                if is_dominated:
                    break

            if not is_dominated:
                if matrix[i][j] not in [p[1] for p in pareto_points]:
                    pareto_points.append(((i, j), matrix[i][j]))

    print("\n2. ОПТИМУМ ЗА ПАРЕТО (КООПЕРАТИВНА):")
    print(pareto_points)
    for (i, j), payoff in pareto_points:
        print(
            f"  Виграш {payoff} (досягається, наприклад, при {blue_strategies[i]} vs {red_strategies[j]})"
        )

    # 5. Обережні стратегії
    blue_min_payoffs = []
    for i in range(n_blue):
        worst_case = min(matrix[i][j][0] for j in range(n_red))
        blue_min_payoffs.append(worst_case)

    maximin_blue_val = max(blue_min_payoffs)
    cautious_blue_indices = [
        i for i, val in enumerate(blue_min_payoffs) if val == maximin_blue_val
    ]

    red_min_payoffs = []
    for j in range(n_red):
        worst_case = min(matrix[i][j][1] for i in range(n_blue))
        red_min_payoffs.append(worst_case)

    maximin_red_val = max(red_min_payoffs)
    cautious_red_indices = [
        j for j, val in enumerate(red_min_payoffs) if val == maximin_red_val
    ]

    print("\n3. ОБЕРЕЖНІ СТРАТЕГІЇ (МАКСИМІН):")
    print(f"  Гарантований виграш Синіх: {maximin_blue_val}")
    print(f"  Стратегії Синіх: {[blue_strategies[i] for i in cautious_blue_indices]}")
    print(f"  Гарантований виграш Червоних: {maximin_red_val}")
    print(
        f"  Стратегії Червоних (перші 5): {[red_strategies[j] for j in cautious_red_indices[:5]]} ... всього {len(cautious_red_indices)}"
    )

    print(f"\n  Гарантований вектор гри (v#): ({maximin_blue_val}, {maximin_red_val})")


if __name__ == "__main__":
    solve_game()
