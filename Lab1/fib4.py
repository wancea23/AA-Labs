import time
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext, ROUND_HALF_EVEN

getcontext().prec = 60

def fib_binet(n):
    phi = Decimal((1 + Decimal(5 ** (1/2))))
    phi2 = Decimal((1 - Decimal(5 ** (1/2))))
    
    result = (phi ** Decimal(n) - phi2 ** Decimal(n)) / (2 ** n * Decimal(5 ** (1/2)))
    return int(result)

def analyze_binet():
    series2 = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162, 3981, 
               5012, 6310, 7943, 10000, 12589, 15849]
    
    results = {'n': [], 'time': [], 'result_digits': []}
    
    print(f"{'n':<10} {'Time (s)':<15} {'Result (digits)':<15}")
    print("-"*70)
    
    for n in series2:
        start_time = time.perf_counter()
        result = fib_binet(n)
        execution_time = time.perf_counter() - start_time
        
        results['n'].append(n)
        results['time'].append(execution_time)
        results['result_digits'].append(len(str(result)))
        
        print(f"{n:<10} {execution_time:<15.6f} {len(str(result)):<15}")
    
    return results

def plot_binet_results(results):
    plt.figure(figsize=(12, 8))
    
    plt.plot(results['n'], results['time'], 'b-o', linewidth=2, markersize=6)
    plt.xlabel('n-th Fibonacci Term', fontsize=12)
    plt.ylabel('Time (s)', fontsize=12)
    plt.title('BINET Formula Fibonacci Function', fontweight='bold', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 16000)
    plt.ylim(0, 0.0012)
    
    plt.axhline(y=0.0012, color='gray', linestyle='-', alpha=0.2)
    plt.axhline(y=0.0010, color='gray', linestyle='-', alpha=0.2)
    plt.axhline(y=0.0008, color='gray', linestyle='-', alpha=0.2)
    plt.axhline(y=0.0006, color='gray', linestyle='-', alpha=0.2)
    plt.axhline(y=0.0004, color='gray', linestyle='-', alpha=0.2)
    plt.axhline(y=0.0002, color='gray', linestyle='-', alpha=0.2)
    
    plt.tight_layout()
    plt.savefig('fib_binet_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    results = analyze_binet()
    plot_binet_results(results)