import numpy as np
import matplotlib.pyplot as plt
import os

def solve_2xn_matrix_game(matrix, save_plot=True, filename=None):
    n = matrix.shape[1]
    
    # Сідлова точка
    row_mins = np.min(matrix, axis=1)
    col_maxs = np.max(matrix, axis=0)
    maximin = np.max(row_mins)
    minimax = np.min(col_maxs)
    has_saddle = maximin == minimax
    
    print(f"Матриця 2×{n}:")
    print(matrix)
    print(f"Максимін α = {maximin}, Мінімакс β = {minimax}")
    print(f"Сідлова точка: {'Так' if has_saddle else 'Ні'}")
    
    # Графічний метод
    x = np.linspace(0, 1, 1000)
    functions = []
    
    for j in range(n):
        coeff = matrix[0, j] - matrix[1, j]
        const = matrix[1, j]
        y = coeff * x + const
        functions.append(y)
    
    lower_envelope = np.minimum.reduce(functions)
    opt_idx = np.argmax(lower_envelope)
    opt_x = x[opt_idx]
    game_value = lower_envelope[opt_idx]
    
    print(f"Оптимальна стратегія: x₁* = {opt_x:.4f}, x₂* = {1-opt_x:.4f}")
    print(f"Значення гри: v = {game_value:.4f}")
    
    # Графік
    if save_plot:
        if not os.path.exists('graphs'):
            os.makedirs('graphs')
        
        plt.figure(figsize=(10, 6))
        
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        for j, func in enumerate(functions):
            plt.plot(x, func, color=colors[j % len(colors)], label=f'M_{j+1}(x)')
        
        plt.plot(x, lower_envelope, 'black', linewidth=3, label='Нижня огинаюча')
        plt.plot(opt_x, game_value, 'ro', markersize=8, label=f'Оптимум ({opt_x:.3f}, {game_value:.3f})')
        
        plt.xlabel('x')
        plt.ylabel('M(x)')
        plt.title(f'Матрична гра 2×{n}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xlim(0, 1)
        
        if filename is None:
            filename = f'graphs/matrix_2x{n}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Графік збережено: {filename}")
    
    return {
        'has_saddle_point': has_saddle,
        'optimal_x': (opt_x, 1-opt_x),
        'game_value': game_value,
        'saved_plot': filename if save_plot else None
    }

def solve_mx2_matrix_game(matrix, save_plot=True, filename=None):
    m = matrix.shape[0]
    
    # Сідлова точка
    row_mins = np.min(matrix, axis=1)
    col_maxs = np.max(matrix, axis=0)
    maximin = np.max(row_mins)
    minimax = np.min(col_maxs)
    has_saddle = maximin == minimax
    
    print(f"Матриця {m}×2:")
    print(matrix)
    print(f"Максимін α = {maximin}, Мінімакс β = {minimax}")
    print(f"Сідлова точка: {'Так' if has_saddle else 'Ні'}")
    
    # Графічний метод
    y = np.linspace(0, 1, 1000)
    functions = []
    
    for i in range(m):
        coeff = matrix[i, 0] - matrix[i, 1]
        const = matrix[i, 1]
        values = coeff * y + const
        functions.append(values)
    
    upper_envelope = np.maximum.reduce(functions)
    opt_idx = np.argmin(upper_envelope)
    opt_y = y[opt_idx]
    game_value = upper_envelope[opt_idx]
    
    print(f"Оптимальна стратегія: y₁* = {opt_y:.4f}, y₂* = {1-opt_y:.4f}")
    print(f"Значення гри: v = {game_value:.4f}")
    
    # Графік
    if save_plot:
        if not os.path.exists('graphs'):
            os.makedirs('graphs')
        
        plt.figure(figsize=(10, 6))
        
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        for i, func in enumerate(functions):
            plt.plot(y, func, color=colors[i % len(colors)], label=f'N_{i+1}(y)')
        
        plt.plot(y, upper_envelope, 'black', linewidth=3, label='Верхня огинаюча')
        plt.plot(opt_y, game_value, 'ro', markersize=8, label=f'Оптимум ({opt_y:.3f}, {game_value:.3f})')
        
        plt.xlabel('y')
        plt.ylabel('N(y)')
        plt.title(f'Матрична гра {m}×2')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xlim(0, 1)
        
        if filename is None:
            filename = f'graphs/matrix_{m}x2.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Графік збережено: {filename}")
    
    return {
        'has_saddle_point': has_saddle,
        'optimal_y': (opt_y, 1-opt_y),
        'game_value': game_value,
        'saved_plot': filename if save_plot else None
    }

def main():
    print("\nЗавдання 1:")
    A1 = np.array([[-40, -25, -10, 0, 5], [-50, -45, -30, -20, -15]])
    r1 = solve_2xn_matrix_game(A1, filename='graphs/1.png')
    
    print("\nЗавдання 2:")
    A2 = np.array([[-40, -39, 2, -1, -7], [-12, 11, -9, 3, -25]])
    r2 = solve_2xn_matrix_game(A2, filename='graphs/2.png')
    
    print("\nЗавдання 3:")
    A3 = np.array([[-40, -20], [-25, -10], [-50, -30]])
    r3 = solve_mx2_matrix_game(A3, filename='graphs/3.png')

    print("\nЗавдання 4:")
    A4 = np.array([[-40, -25], [-15, -35], [-5, -20]])
    r4 = solve_mx2_matrix_game(A4, filename='graphs/4.png')
    
    return [r1, r2, r3, r4]

# Приклад використання
if __name__ == "__main__":
    # Створити всі завдання для варіанту 10
    results = main()
    
    # Або розв'язати одну матрицю
    # A = np.array([[1, 2, 3], [4, 5, 6]])
    # result = solve_2xn_matrix_game(A)