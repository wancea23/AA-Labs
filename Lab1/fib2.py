import time
import matplotlib.pyplot as plt
import numpy as np

class DynamicFibonacci:
    def __init__(self):
        self.operations = 0
        self.execution_time = 0
    
    def fibonacci(self, n):
        self.operations = 0
        if n <= 1:
            return n
        
        dp = [0] * (n + 1)
        dp[1] = 1
        
        for i in range(2, n + 1):
            dp[i] = dp[i-1] + dp[i-2]
            self.operations += 1
        return dp[n]
    
    def calculate(self, n):
        start_time = time.perf_counter()
        result = self.fibonacci(n)
        self.execution_time = time.perf_counter() - start_time
        return result

def analyze_dp():
    series2 = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162, 3981, 
               5012, 6310, 7943, 10000, 12589, 15849]
    
    fib = DynamicFibonacci()
    results = {'n': [], 'time': [], 'operations': [], 'result_digits': []}
    
    print("\n" + "-"*70)
    print("SERIES 2 - Large Input Sizes (DP Method)")
    print("-"*70)
    print(f"{'n':<10} {'Time (s)':<15} {'Operations':<15} {'Result (digits)':<15}")
    print("-"*70)
    
    for n in series2:
        result = fib.calculate(n)
        results['n'].append(n)
        results['time'].append(fib.execution_time)
        results['operations'].append(fib.operations)
        results['result_digits'].append(len(str(result)))
        
        print(f"{n:<10} {fib.execution_time:<15.6f} {fib.operations:<15} {len(str(result)):<15}")
    
    return results

def plot_dp_results(results):
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    ax = axes[0]
    ax.plot(results['n'], results['time'], 'g-o', linewidth=2, markersize=8)
    ax.set_xlabel('n (Fibonacci term)')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('DP Fibonacci - Time Complexity', fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    ax = axes[1]
    ax.plot(results['n'], results['operations'], 'b-s', linewidth=2, markersize=8)
    ax.set_xlabel('n (Fibonacci term)')
    ax.set_ylabel('Number of Operations')
    ax.set_title('DP Fibonacci - Operations Count', fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    n = np.array(results['n'])
    ax.plot(n, n, 'r--', linewidth=2, label='Theoretical O(n)')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('fib_dp_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    results = analyze_dp()
    plot_dp_results(results)