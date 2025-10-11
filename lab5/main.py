import pulp
import numpy as np

A = np.array([
    [ 1, -2,  3, -4,  5],
    [-3,  4, -1,  2,  0],
    [ 2, -3,  0,  5, -2],
    [ 0,  1, -4,  3, -3]
])

print("Початкова платіжна матриця A:")
print(A)

min_val = np.min(A)
k = 0
if min_val <= 0:
    k = abs(min_val) + 1  # Додаємо 1 для гарантії, що всі > 0
    
A_prime = A + k
print(f"\nКонстанта для зсуву k = {k}")
print("Модифікована матриця A':")
print(A_prime)

m, n = A_prime.shape

prob_p1 = pulp.LpProblem("Player1_Game", pulp.LpMinimize)

x_vars = [pulp.LpVariable(f'x{i}', lowBound=0) for i in range(m)]

prob_p1 += pulp.lpSum(x_vars), "Minimize_1/V"

for j in range(n):
    constraint = pulp.lpSum([A_prime[i][j] * x_vars[i] for i in range(m)]) >= 1
    prob_p1 += constraint, f"Constraint_P2_strategy_{j}"

prob_p1.solve(pulp.PULP_CBC_CMD(msg=0))

if pulp.LpStatus[prob_p1.status] == 'Optimal':
    # Оптимальне значення 1/V
    one_over_V = pulp.value(prob_p1.objective)
    
    V = 1 / one_over_V
    
    p_strategy = [var.varValue * V for var in x_vars]
    
    initial_V = V - k
    
    print("\n--- Результати ---")
    print(f"Ціна гри (скоригована): {initial_V:.4f}")
    
    print("\nОптимальна змішана стратегія для Гравця 1 (ймовірності p_i):")
    for i, p in enumerate(p_strategy):
        print(f"  Стратегія {i+1}: {p:.4f}")

    q_strategy = []
    for name, c in prob_p1.constraints.items():
        q_strategy.append(c.pi * V)
        
    print("\nОптимальна змішана стратегія для Гравця 2 (ймовірності q_j):")
    for j, q in enumerate(q_strategy):
        print(f"  Стратегія {j+1}: {q:.4f}")

else:
    print("Не вдалося знайти оптимальний розв'язок.")