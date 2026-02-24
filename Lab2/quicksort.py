import random
import time
import matplotlib.pyplot as plt
import sys
import numpy as np

sys.setrecursionlimit(20000)

class QuickSort:
    def __init__(self):
        self.comparisons = 0
        self.swaps = 0
        self.execution_time = 0
    
    def sort(self, arr):
        self.comparisons = 0
        self.swaps = 0
        arr_copy = arr.copy()
        
        start_time = time.perf_counter()
        self._quick_sort(arr_copy, 0, len(arr_copy) - 1)
        self.execution_time = time.perf_counter() - start_time
        
        return arr_copy
    
    def _quick_sort(self, arr, low, high):
        if low < high:
            pi = self._partition(arr, low, high)
            self._quick_sort(arr, low, pi - 1)
            self._quick_sort(arr, pi + 1, high)
    
    def _partition(self, arr, low, high):
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            self.comparisons += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                self.swaps += 1
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        self.swaps += 1
        return i + 1

def generate_datasets():
    series = [100, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
               12000, 14000, 16000, 18000]
    
    datasets = {
        'random': {},
        'sorted': {},
        'reverse': {},
        'partial': {}
    }
    
    for size in series:

        datasets['random'][size] = [random.randint(1, 10000) for _ in range(size)]
        datasets['sorted'][size] = list(range(size))
        datasets['reverse'][size] = list(range(size, 0, -1))
        
        # Partially sorted (70% sorted, 30% random)
        arr = list(range(size))
        shuffle_count = size // 3
        for _ in range(shuffle_count):
            i, j = random.randint(0, size-1), random.randint(0, size-1)
            arr[i], arr[j] = arr[j], arr[i]
        datasets['partial'][size] = arr
    
    return series, datasets

def analyze_quick_sort():
    qs = QuickSort()
    series, datasets = generate_datasets()
    
    # Results storage
    results = {
        'data_types': {}
    }
    
    for data_type in ['random', 'sorted', 'reverse', 'partial']:
        results['data_types'][data_type] = {}
        for size in series:
            results['data_types'][data_type][size] = {'time': 0, 'comparisons': 0, 'swaps': 0}
    
    for data_type in ['random', 'sorted', 'reverse', 'partial']:
        print(f"\n{data_type.upper()} DATA:")
        print(f"{'n':<10} {'Time (s)':<15} {'Comparisons':<15} {'Swaps':<15}")
        print("-"*55)
        
        for size in series:
            data = datasets[data_type][size]
            qs.sort(data)
            results['data_types'][data_type][size]['time'] = qs.execution_time
            results['data_types'][data_type][size]['comparisons'] = qs.comparisons
            results['data_types'][data_type][size]['swaps'] = qs.swaps
            print(f"{size:<10} {qs.execution_time:<15.6f} {qs.comparisons:<15} {qs.swaps:<15}")
    
    return results, series

def plot_results(results, series):
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    sizes = list(series)
    
    # Time comparison for all data types
    ax = axes[0, 0]
    colors = {'random': 'blue', 'sorted': 'green', 'reverse': 'red', 'partial': 'orange'}
    markers = {'random': 'o', 'sorted': 's', 'reverse': '^', 'partial': 'd'}
    
    for data_type in ['random', 'sorted', 'reverse', 'partial']:
        times = [results['data_types'][data_type][s]['time'] for s in sizes]
        ax.plot(sizes, times, color=colors[data_type], marker=markers[data_type], 
                linewidth=2, markersize=6, label=data_type.capitalize())
    
    ax.set_xlabel('Input Size (n)')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Quick Sort - Time Complexity by Data Type', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Comparisons comparison
    ax = axes[0, 1]
    for data_type in ['random', 'sorted', 'reverse', 'partial']:
        comparisons = [results['data_types'][data_type][s]['comparisons'] for s in sizes]
        ax.plot(sizes, comparisons, color=colors[data_type], marker=markers[data_type], 
                linewidth=2, markersize=6, label=data_type.capitalize())
    
    ax.set_xlabel('Input Size (n)')
    ax.set_ylabel('Number of Comparisons')
    ax.set_title('Quick Sort - Comparisons by Data Type', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Swaps comparison
    ax = axes[1, 0]
    for data_type in ['random', 'sorted', 'reverse', 'partial']:
        swaps = [results['data_types'][data_type][s]['swaps'] for s in sizes]
        ax.plot(sizes, swaps, color=colors[data_type], marker=markers[data_type], 
                linewidth=2, markersize=6, label=data_type.capitalize())
    
    ax.set_xlabel('Input Size (n)')
    ax.set_ylabel('Number of Swaps')
    ax.set_title('Quick Sort - Swaps by Data Type', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Theoretical vs Actual (Random data)
    ax = axes[1, 1]
    n = np.array(sizes)
    
    # Get actual times for random data
    actual_times = [results['data_types']['random'][s]['time'] for s in sizes]
    
    # Calculate n log n for reference
    n_log_n = n * np.log2(n)
    if actual_times[-1] > 0:
        # Normalize to match the scale of actual times
        n_log_n = n_log_n / n_log_n[-1] * actual_times[-1]
    
    ax.plot(sizes, actual_times, 'b-o', linewidth=2, markersize=8, label='Actual (Random)')
    ax.plot(sizes, n_log_n, 'r--', linewidth=2, label='n log n Reference')
    ax.set_xlabel('Input Size (n)')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Quick Sort - Theoretical vs Actual', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('quick_sort_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    results, series = analyze_quick_sort()
    plot_results(results, series)