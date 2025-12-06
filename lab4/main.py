import math
from itertools import combinations

V = {
    (1,): 80,
    (2,): 130,
    (3,): 180,
    (1, 2): 240,
    (1, 3): 280,
    (2, 3): 350,
    (1, 2, 3): 480,
    (): 0,
}

PLAYERS = [1, 2, 3]
NUM_PLAYERS = len(PLAYERS)

CHOSEN_X_PRIME = {1: 1 / 4, 2: 1 / 3, 3: 1 / 3}


def check_properties():
    print("--- 1. Властивості гри ---")

    is_superadditive = True
    print("Перевірка суперадитивності:")
    for p1, p2 in combinations(PLAYERS, 2):
        s_val = V[(p1,)] + V[(p2,)]
        union_val = V[(p1, p2)]
        sign = "<" if s_val < union_val else ">="  # Строга нерівність теж ок
        print(f"  V({p1}) + V({p2}) = {s_val} {sign} V({p1},{p2})={union_val}")
        if s_val > union_val:
            is_superadditive = False

    grand_val = V[tuple(PLAYERS)]
    if is_superadditive:
        print("-> Характеристична функція є суперадитивною.")

    sum_individual = sum(V[(i,)] for i in PLAYERS)

    print("\nПеревірка істотності:")
    print(f"  Сума V(i) = {sum_individual}")
    print(f"  V(N) = {grand_val}")

    if sum_individual < grand_val:
        k_prime = grand_val - sum_individual
        print(f"-> Гра є істотною. k' = {grand_val} - {sum_individual} = {k_prime}")
        return True, k_prime
    else:
        print("-> Гра не є істотною.")
        return False, 0


# --- Крок 2: 0-1 спрощена форма ---
def analyze_01_form(k_prime):
    print("\n--- 2. 0-1 спрощена форма ---")
    print(f"Формула: V'(S) = (V(S) - Sum V(i)) / k'")

    V_prime = {}

    # Для одноелементних завжди 0, для повної 1
    for i in PLAYERS:
        V_prime[(i,)] = 0
    V_prime[tuple(PLAYERS)] = 1

    print(f"  V'(1) = V'(2) = V'(3) = 0")
    print(f"  V'(1,2,3) = 1")

    # Розрахунок для пар
    for coalition in combinations(PLAYERS, 2):
        sum_v_i = sum(V[(i,)] for i in coalition)
        val_prime = (V[coalition] - sum_v_i) / k_prime
        V_prime[coalition] = val_prime

        calc_str = f"({V[coalition]} - {sum_v_i}) / {k_prime}"
        print(f"  V'{coalition} = {calc_str} = {val_prime:.4f}")

    return V_prime


# --- Крок 3: Перевірка С-ядра ---
def check_core_conditions(V_prime):
    print("\n--- 3. Перевірка умов непорожнечі С-ядра ---")
    # Умова достаттності: V'(S) <= 1 / (n - |S| + 1)
    limit_2 = 1 / (3 - 2 + 1)  # 0.5

    possible = True
    for coalition in combinations(PLAYERS, 2):
        val = V_prime[coalition]
        status = "OK" if val <= limit_2 else "Порушення достатньої умови"
        print(f"  V'{coalition} = {val:.4f} <= {limit_2} -> {status}")
        if val > limit_2:
            possible = False

    if possible:
        print("-> С-ядро непорожнє (достатні умови виконуються).")


# --- Крок 4: Вектор Шеплі ---
def calculate_shapley_value():
    print("\n--- 4. Вектор Шеплі ---")
    shapley_values = {p: 0 for p in PLAYERS}
    factorial_n = math.factorial(NUM_PLAYERS)

    for player in PLAYERS:
        for r in range(1, NUM_PLAYERS + 1):
            for coalition in combinations(PLAYERS, r):
                if player in coalition:
                    # Коаліція без гравця
                    coalition_without = tuple(
                        sorted(list(p for p in coalition if p != player))
                    )

                    marginal = V.get(coalition, 0) - V.get(coalition_without, 0)

                    s_len = len(coalition)
                    weight = (
                        math.factorial(s_len - 1) * math.factorial(NUM_PLAYERS - s_len)
                    ) / factorial_n

                    shapley_values[player] += weight * marginal

    print("Розподіл за Шеплі:")
    for p, val in shapley_values.items():
        print(f"  Гравець {p}: {val:.2f}")

    print("Перевірка належності вектора Шеплі С-ядру:")
    in_core = True
    for r in range(2, NUM_PLAYERS):
        for coalition in combinations(PLAYERS, r):
            sum_x = sum(shapley_values[p] for p in coalition)
            v_s = V[coalition]
            status = "OK" if sum_x >= v_s - 0.01 else "Блокує (не в ядрі)"
            print(f"  S={coalition}: Сума={sum_x:.2f} >= V(S)={v_s} -> {status}")
            if sum_x < v_s - 0.01:
                in_core = False


# --- Крок 5: Розрахунок X через X' ---
def solve_final_vector(V_prime, k_prime):
    print("\n--- 5. Розрахунок вектора X (за обраним X') ---")

    x_prime = CHOSEN_X_PRIME
    print(f"Обраний вектор X' = ({x_prime[1]:.3f}, {x_prime[2]:.3f}, {x_prime[3]:.3f})")

    # Перевірка чи X' підходить
    fits = True
    for coalition, val in V_prime.items():
        if len(coalition) == 2:
            s_xp = sum(x_prime[i] for i in coalition)
            if s_xp < val - 0.001:
                print(f"  УВАГА: X' порушує умову для {coalition}")
                fits = False

    if fits:
        print("  Вектор X' задовольняє умови С-ядра.")

    print(f"\nПерехід до реальних виплат: x_i = k' * x'_i + V(i)")
    total_sum = 0
    for i in PLAYERS:
        c_prime = V[(i,)]
        val = k_prime * x_prime[i] + c_prime
        total_sum += val
        print(f"  x_{i} = {k_prime} * {x_prime[i]:.3f} + {c_prime} = {val:.2f}")

    print(f"Сума: {total_sum:.2f} (Має бути {V[tuple(PLAYERS)]})")


if __name__ == "__main__":
    is_essential, k_val = check_properties()

    if is_essential:
        v_prime_data = analyze_01_form(k_val)
        check_core_conditions(v_prime_data)
        calculate_shapley_value()
        solve_final_vector(v_prime_data, k_val)
