import time
import matplotlib.pyplot as plt
import numpy as np

class MatrixFibonacci:
    def __init__(self):
        self.multiplications = 0
        self.execution_time = 0
    
    def matrix_multiply(self, A, B):
        self.multiplications += 8
        return [
            [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
            [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]
        ]
    
    def matrix_power(self, M, n):
        if n == 1:
            return M
        
        if n % 2 == 0:
            half = self.matrix_power(M, n // 2)
            return self.matrix_multiply(half, half)
        else:
            half = self.matrix_power(M, (n - 1) // 2)
            half_sq = self.matrix_multiply(half, half)
            return self.matrix_multiply(M, half_sq)
    
    def fibonacci(self, n):
        self.multiplications = 0
        if n <= 1:
            return n
        
        M = [[0, 1], [1, 1]]
        
        result_matrix = self.matrix_power(M, n)
        
        return result_matrix[0][1]
    
    def calculate(self, n):
        start_time = time.perf_counter()
        result = self.fibonacci(n)
        self.execution_time = time.perf_counter() - start_time
        return result

def analyze_matrix():
    
    series2 = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162, 3981, 
               5012, 6310, 7943, 10000, 12589, 15849]
    
    fib = MatrixFibonacci()
    results = {'n': [], 'time': [], 'multiplications': [], 'result_digits': []}
    
    print("\n" + "-"*70)
    print("SERIES 2 - Large Input Sizes (Matrix Method)")
    print("-"*70)
    print(f"{'n':<10} {'Time (s)':<15} {'Multiplications':<15} {'Result (digits)':<15}")
    print("-"*70)
    
    for n in series2:
        result = fib.calculate(n)
        results['n'].append(n)
        results['time'].append(fib.execution_time)
        results['multiplications'].append(fib.multiplications)
        results['result_digits'].append(len(str(result)))
        
        print(f"{n:<10} {fib.execution_time:<15.6f} {fib.multiplications:<15} {len(str(result)):<15}")
    
    return results

def plot_matrix_results(results):
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    ax = axes[0]
    ax.plot(results['n'], results['time'], 'm-o', linewidth=2, markersize=8)
    ax.set_xlabel('n (Fibonacci term)')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Matrix Fibonacci - Logarithmic Time', fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    ax = axes[1]
    ax.plot(results['n'], results['multiplications'], 'c-s', linewidth=2, markersize=8)
    ax.set_xlabel('n (Fibonacci term)')
    ax.set_ylabel('Number of Matrix Multiplications')
    ax.set_title('Matrix Fibonacci - Multiplications Count', fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    n = np.array(results['n'])
    log_n = 8 * np.log2(n)
    ax.plot(n, log_n, 'r--', linewidth=2, label='Theoretical O(log n)')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('fib_matrix_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    results = analyze_matrix()
    plot_matrix_results(results)