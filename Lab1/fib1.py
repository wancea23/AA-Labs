import time
import matplotlib.pyplot as plt
import sys

sys.setrecursionlimit(10000)

class RecursiveFibonacci:
    def __init__(self):
        self.calls = 0
        self.execution_time = 0
    
    def fibonacci(self, n):
        self.calls += 1
        if n <= 1:
            return n
        return self.fibonacci(n-1) + self.fibonacci(n-2)
    
    def calculate(self, n):
        self.calls = 0
        start_time = time.perf_counter()
        result = self.fibonacci(n)
        self.execution_time = time.perf_counter() - start_time
        return result

def analyze_recursive():
    series1 = [5, 7, 10, 12, 15, 17, 20, 22, 25, 27, 30, 32, 35, 37, 40, 42, 45]
    
    fib = RecursiveFibonacci()
    results = {'n': [], 'time': [], 'calls': [], 'result': []}

    print(f"{'n':<10} {'Time (s)':<15} {'Calls':<15} {'Result':<20}")
    print("-"*70)
    
    for n in series1:
        result = fib.calculate(n)
        results['n'].append(n)
        results['time'].append(fib.execution_time)
        results['calls'].append(fib.calls)
        results['result'].append(result)
        
        print(f"{n:<10} {fib.execution_time:<15.6f} {fib.calls:<15} {result:<20}")
    
    return results

def plot_recursive_results(results):
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Time complexity
    ax = axes[0]
    ax.plot(results['n'], results['time'], 'r-o', linewidth=2, markersize=8)
    ax.set_xlabel('n (Fibonacci term)')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Recursive Fibonacci - Time Complexity', fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Number of calls
    ax = axes[1]
    ax.plot(results['n'], results['calls'], 'b-s', linewidth=2, markersize=8)
    ax.set_xlabel('n (Fibonacci term)')
    ax.set_ylabel('Number of Function Calls')
    ax.set_title('Recursive Fibonacci - Number of Calls', fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('fib_recursive_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    results = analyze_recursive()
    plot_recursive_results(results)
