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
    (): 0
}

PLAYERS = [1, 2, 3]
NUM_PLAYERS = len(PLAYERS)

# --- Крок 1: Перевірка властивостей гри ---
def check_properties():
    print("--- 1. Властивості гри ---")
    
    # Суперадитивність
    is_superadditive = True
    if V[(1, 2)] < V[(1,)] + V[(2,)]: is_superadditive = False
    if V[(1, 3)] < V[(1,)] + V[(3,)]: is_superadditive = False
    if V[(2, 3)] < V[(2,)] + V[(3,)]: is_superadditive = False
    if V[(1, 2, 3)] < V[(1,)] + V[(2, 3)]: is_superadditive = False
    
    if is_superadditive:
        print("Суперадитивність: Так (об'єднуватися вигідно).")
    else:
        print("Суперадитивність: Ні.")

    # Істотність
    sum_individual = V[(1,)] + V[(2,)] + V[(3,)]
    grand_coalition = V[(1, 2, 3)]
    
    if sum_individual < grand_coalition:
        print(f"Істотність: Так (додатковий виграш: {grand_coalition - sum_individual}).\n")
    else:
        print("Істотність: Ні.\n")

# --- Крок 2: 0-1 спрощена форма та С-ядро ---
def analyze_01_form_and_core():
    print("--- 2. 0-1 спрощена форма та аналіз С-ядра ---")
    
    sum_individual = V[(1,)] + V[(2,)] + V[(3,)]
    grand_coalition = V[(1, 2, 3)]
    denominator = grand_coalition - sum_individual
    
    if denominator == 0:
        print("Неможливо виконати аналіз, гра не є істотною.")
        return

    # Розрахунок V'
    V_prime = {}
    for r in range(1, NUM_PLAYERS + 1):
        for coalition in combinations(PLAYERS, r):
            sum_v_i = sum(V.get((i,), 0) for i in coalition)
            V_prime[coalition] = (V[coalition] - sum_v_i) / denominator

    print("Значення V' (0-1 форма):")
    for coalition, value in V_prime.items():
        print(f"  V'{coalition} = {value:.3f}")

    # Перевірка С-ядра
    is_core_non_empty = True
    for r in range(1, NUM_PLAYERS):
        for coalition in combinations(PLAYERS, r):
            limit = 1 / (NUM_PLAYERS - len(coalition) + 1)
            if V_prime[coalition] > limit:
                is_core_non_empty = False
    
    if is_core_non_empty:
        print("\nС-ядро: Не є порожнім (існують стабільні розподіли).\n")
    else:
        print("\nС-ядро: Умова непорожнечі не виконується.\n")
        
# --- Крок 3: Розрахунок вектора Шеплі ---
def calculate_shapley_value():
    print("--- 3. Вектор Шеплі ---")
    shapley_values = {p: 0 for p in PLAYERS}

    for player in PLAYERS:
        for r in range(1, NUM_PLAYERS + 1):
            for coalition in combinations(PLAYERS, r):
                if player in coalition:
                    coalition_without_player = tuple(p for p in coalition if p != player)
                    marginal_contribution = V[coalition] - V.get(coalition_without_player, 0)
                    weight = (math.factorial(len(coalition) - 1) * math.factorial(NUM_PLAYERS - len(coalition))) / math.factorial(NUM_PLAYERS)
                    shapley_values[player] += weight * marginal_contribution

    print("Справедливий розподіл виграшу:")
    for player, value in shapley_values.items():
        print(f"  Гравець {player}: {value:.2f}")
    
    print(f"\nПеревірка суми: {sum(shapley_values.values()):.2f} (загальний виграш: {V[(1, 2, 3)]})")

if __name__ == "__main__":
    check_properties()
    analyze_01_form_and_core()
    calculate_shapley_value()