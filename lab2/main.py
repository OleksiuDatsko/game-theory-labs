from tabulate import tabulate
import matplotlib.pyplot as plt

def solve_matrix_game_fictitious_play(payoff_matrix, N_iterations):
    A = payoff_matrix
    m = len(A)
    n = len(A[0])

    i_k = 0
    j_k = 0

    # Лічильники використання чистих стратегій
    counter_A = [0] * m
    counter_B = [0] * n

    # Зберігання результатів
    history = []

    for k in range(N_iterations):
        counter_A[i_k] += 1
        counter_B[j_k] += 1

        current_k = k + 1  # Поточний номер ітерації

        p_k = [count / current_k for count in counter_A]
        q_k = [count / current_k for count in counter_B]

        max_a = -float("inf")
        for i in range(m):
            expected_ai = sum(A[i][j] * q_k[j] for j in range(n))

            if expected_ai > max_a:
                max_a = expected_ai
                i_k = i

        min_b = float("inf")
        for j in range(n):
            expected_bj = sum(A[i][j] * p_k[i] for i in range(m))

            if expected_bj < min_b:
                min_b = expected_bj
                j_k = j

        v_k = (max_a + min_b) / 2

        history.append(
            {
                "k": current_k,
                "i_k": i_k + 1,
                "j_k": j_k + 1,
                "p_k": [f"{x:.1f}" for x in p_k],
                "q_k": [f"{x:.1f}" for x in q_k],
                "a_k": max_a,
                "b_k": min_b,
                "v_k": v_k,
            }
        )

    return history, p_k, q_k, v_k


A = [
        [0, 0, 1],
        [3, 2, 4],
        [0, 2, 3],
        [5, -1, -3],
        [-3, 2, -3],
]
N = 10

results, p_star, q_star, final_value = solve_matrix_game_fictitious_play(A, N)


print("\n" + "=" * 120)
print(f"МЕТОД ФІКТИВНОГО РОЗІГРАШУ (N={N} ітерацій)")
print(tabulate(A))
print("=" * 120)

header = results[0].keys()
rows = [x.values() for x in results]
print(tabulate(rows, header))


print("-" * 120)
print(f"ФІНАЛЬНІ РЕЗУЛЬТАТИ ПІСЛЯ {N} ІТЕРАЦІЙ:")
print(f"Наближена ціна гри (v): {final_value:.4f}")
print(f"Наближена стратегія Гравця A (p*): {p_star}")
print(f"Наближена стратегія Гравця B (q*): {q_star}")
print("=" * 120)


# --- ПОБУДОВА ГРАФІКА ---

k_values = [res['k'] for res in results]
v_lower_values = [res['a_k'] for res in results]
v_upper_values = [res['b_k'] for res in results]
v_avg_values = [res['v_k'] for res in results]

plt.figure(figsize=(12, 6))

plt.plot(k_values, v_lower_values, label=r'$\alpha_k$ (Нижня оцінка', color='blue', linestyle='-')
plt.plot(k_values, v_upper_values, label=r'$\beta_k$ (Верхня оцінка', color='red', linestyle='--')
plt.plot(k_values, v_avg_values, label=r'$v_k = (\alpha_k + \beta_k)/2$', color='green', linestyle='-', linewidth=2)

plt.title(f'Метод Фіктивного Розіграшу: Збіжність Ціни Гри (N={N})')
plt.xlabel('Номер ітерації (k)')
plt.ylabel('Оцінка ціни гри')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.axhline(final_value, color='purple', linestyle=':', alpha=0.7, label=f'v_final ≈ {final_value:.4f}')

plt.savefig('game_value_convergence.png') # Зберегти графік у файл
