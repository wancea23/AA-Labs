import random
import time
import matplotlib.pyplot as plt
import sys
import numpy as np

class BubbleSort:
    def __init__(self):
        self.comparisons = 0
        self.swaps = 0
        self.execution_time = 0
    
    def sort(self, arr):
        self.comparisons = 0
        self.swaps = 0
        arr_copy = arr.copy()
        n = len(arr_copy)
        
        start_time = time.perf_counter()
        
        for i in range(n):
            for j in range(0, n - i - 1):
                self.comparisons += 1
                if arr_copy[j] > arr_copy[j + 1]:
                    arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                    self.swaps += 1
        
        self.execution_time = time.perf_counter() - start_time
        
        return arr_copy

def generate_datasets():
    series1 = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 
               1200, 1400, 1600, 1800, 2000]
    
    series2 = [2000, 3000, 4000, 5000, 6000]
    
    datasets = {
        'random': {},
        'sorted': {},
        'reverse': {},
        'partial': {}
    }
    
    print("Generating datasets...")
    for size in series1 + series2:
        if size % 2000 == 0:
            print(f"  Generating size {size}...")
        datasets['random'][size] = [random.randint(1, 10000) for _ in range(size)]
        datasets['sorted'][size] = list(range(size))
        datasets['reverse'][size] = list(range(size, 0, -1))
        
        arr = list(range(size))
        shuffle_count = size // 3
        for _ in range(shuffle_count):
            i, j = random.randint(0, size-1), random.randint(0, size-1)
            arr[i], arr[j] = arr[j], arr[i]
        datasets['partial'][size] = arr
    
    return series1, series2, datasets

def analyze_bubble_sort():
    print("="*70)
    print("BUBBLE SORT EMPIRICAL ANALYSIS")
    print("="*70)
    
    bs = BubbleSort()
    series1, series2, datasets = generate_datasets()
    
    results = {
        'series1': {},
        'series2': {},
        'data_types': {}
    }
    
    for size in series1:
        results['series1'][size] = {'time': 0, 'comparisons': 0, 'swaps': 0}
    
    for size in series2:
        results['series2'][size] = {'time': 0, 'comparisons': 0, 'swaps': 0}
    
    for data_type in ['random', 'sorted', 'reverse', 'partial']:
        results['data_types'][data_type] = {}
        for size in series2:
            results['data_types'][data_type][size] = {'time': 0, 'comparisons': 0, 'swaps': 0}
    
    print("\n" + "-"*70)
    print("SERIES 1 - Smaller Input Sizes (Random Data)")
    print("-"*70)
    print(f"{'n':<10} {'Time (s)':<15} {'Comparisons':<15} {'Swaps':<15}")
    print("-"*70)
    
    for size in series1:
        data = datasets['random'][size]
        bs.sort(data)
        results['series1'][size]['time'] = bs.execution_time
        results['series1'][size]['comparisons'] = bs.comparisons
        results['series1'][size]['swaps'] = bs.swaps
        print(f"{size:<10} {bs.execution_time:<15.6f} {bs.comparisons:<15} {bs.swaps:<15}")
    
    for data_type in ['random', 'sorted', 'reverse', 'partial']:
        print(f"\n{data_type.upper()} DATA:")
        print(f"{'n':<10} {'Time (s)':<15} {'Comparisons':<15} {'Swaps':<15}")
        print("-"*55)
        
        for size in series2:
            data = datasets[data_type][size]
            bs.sort(data)
            results['data_types'][data_type][size]['time'] = bs.execution_time
            results['data_types'][data_type][size]['comparisons'] = bs.comparisons
            results['data_types'][data_type][size]['swaps'] = bs.swaps
            print(f"{size:<10} {bs.execution_time:<15.6f} {bs.comparisons:<15} {bs.swaps:<15}")
    
    return results, series1, series2

def plot_results(results, series1, series2):
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    ax = axes[0, 0]
    sizes = list(results['series1'].keys())
    times = [results['series1'][s]['time'] for s in sizes]
    ax.plot(sizes, times, 'g-o', linewidth=2, markersize=8)
    ax.set_xlabel('Input Size (n)')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Bubble Sort Time Complexity - Series 1', fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    ax = axes[0, 1]
    comparisons = [results['series1'][s]['comparisons'] for s in sizes]
    ax.plot(sizes, comparisons, 'b-s', linewidth=2, markersize=8)
    ax.set_xlabel('Input Size (n)')
    ax.set_ylabel('Number of Comparisons')
    ax.set_title('Bubble Sort Comparisons - Series 1', fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    ax = axes[1, 0]
    sizes = list(results['data_types']['random'].keys())
    colors = {'random': 'blue', 'sorted': 'green', 'reverse': 'red', 'partial': 'orange'}
    markers = {'random': 'o', 'sorted': 's', 'reverse': '^', 'partial': 'd'}
    
    for data_type in ['random', 'sorted', 'reverse', 'partial']:
        times = [results['data_types'][data_type][s]['time'] for s in sizes]
        ax.plot(sizes, times, color=colors[data_type], marker=markers[data_type],
                linewidth=2, markersize=6, label=data_type.capitalize())
    
    ax.set_xlabel('Input Size (n)')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Bubble Sort - Performance by Data Type', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    ax = axes[1, 1]
    n = np.array(sizes)
    
    actual_times = [results['data_types']['random'][s]['time'] for s in sizes]
    
    n_squared = n ** 2
    if actual_times[-1] > 0:
        n_squared = n_squared / n_squared[-1] * actual_times[-1]
    
    ax.plot(sizes, actual_times, 'g-o', linewidth=2, markersize=8, label='Actual (Random)')
    ax.plot(sizes, n_squared, 'r--', linewidth=2, label='n² Reference')
    ax.set_xlabel('Input Size (n)')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Bubble Sort - Theoretical vs Actual', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('bubble_sort_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    results, series1, series2 = analyze_bubble_sort()
    plot_results(results, series1, series2)