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
    
    # Графічний метод - ВИПРАВЛЕНО: рядок 1 зліва (x=0), рядок 2 справа (x=1)
    x = np.linspace(0, 1, 1000)
    functions = []
    
    for j in range(n):
        coeff = matrix[1, j] - matrix[0, j]
        const = matrix[0, j]
        y = coeff * x + const
        functions.append(y)
    
    lower_envelope = np.minimum.reduce(functions)
    opt_idx = np.argmax(lower_envelope)
    opt_x = x[opt_idx]
    game_value = lower_envelope[opt_idx]
    
    print(f"Оптимальна стратегія: x₁* = {1-opt_x:.4f}, x₂* = {opt_x:.4f}")
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
        
        plt.xlabel('x₂')
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
        'optimal_x': (1-opt_x, opt_x),
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
    
    y = np.linspace(0, 1, 1000)
    functions = []
    
    for i in range(m):
        coeff = matrix[i, 1] - matrix[i, 0]
        const = matrix[i, 0]
        values = coeff * y + const
        functions.append(values)
    
    upper_envelope = np.maximum.reduce(functions)
    opt_idx = np.argmin(upper_envelope)
    opt_y = y[opt_idx]
    game_value = upper_envelope[opt_idx]
    
    # y тут це y2, тому y1 = 1-y
    print(f"Оптимальна стратегія: y₁* = {1-opt_y:.4f}, y₂* = {opt_y:.4f}")
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
        
        plt.xlabel('y₂ (Ліва колонка ← → Права колонка)')
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
        'optimal_y': (1-opt_y, opt_y),
        'game_value': game_value,
        'saved_plot': filename if save_plot else None
    }


def main():
    # ВАРІАНТ 9 з методички
    print("\nЗавдання 1:")
    A1 = np.array([[5, 2, 4, 5, 24], 
                   [5, 5, 11, 5, 19]])
    r1 = solve_2xn_matrix_game(A1, filename='lab3/graphs/1.png')
    
    print("\nЗавдання 2:")
    A2 = np.array([[23, 25, 40, 25, 14], 
                   [15, 40, 25, 14, 24]])
    r2 = solve_2xn_matrix_game(A2, filename='lab3/graphs/2.png')
    
    print("\nЗавдання 3:")
    A3 = np.array([[5, 4], 
                   [2, 11], 
                   [4, 5], 
                   [5, 24]])
    r3 = solve_mx2_matrix_game(A3, filename='lab3/graphs/3.png')

    print("\nЗавдання 4:")
    A4 = np.array([[10, 40], 
                   [25, 35], 
                   [40, 25], 
                   [25, 14]])
    r4 = solve_mx2_matrix_game(A4, filename='lab3/graphs/4.png')
    
    return [r1, r2, r3, r4]


if __name__ == "__main__":
    results = main()
