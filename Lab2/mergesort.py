# merge_sort_analysis.py
import random
import time
import matplotlib.pyplot as plt
import sys
import numpy as np

sys.setrecursionlimit(20000)

class MergeSort:
    def __init__(self):
        self.comparisons = 0
        self.merges = 0
        self.execution_time = 0
    
    def sort(self, arr):
        self.comparisons = 0
        self.merges = 0
        arr_copy = arr.copy()
        
        start_time = time.perf_counter()
        self._merge_sort(arr_copy)
        self.execution_time = time.perf_counter() - start_time
        
        return arr_copy
    
    def _merge_sort(self, arr):
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]
        
        left = self._merge_sort(left)
        right = self._merge_sort(right)
        
        return self._merge(left, right, arr)
    
    def _merge(self, left, right, arr):
        i = j = k = 0
        
        while i < len(left) and j < len(right):
            self.comparisons += 1
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
        
        self.merges += 1
        return arr

def generate_datasets():
    """Generate two series of input data similar to Fibonacci lab"""
    
    # First series - smaller sizes for detailed analysis
    series1 = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 
               1200, 1400, 1600, 1800, 2000]
    
    # Second series - larger sizes for performance comparison
    series2 = [2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000,
               12000, 14000, 16000, 18000, 20000]
    
    # Generate different types of data for each size
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
        
        # Partially sorted (70% sorted, 30% random)
        arr = list(range(size))
        shuffle_count = size // 3
        for _ in range(shuffle_count):
            i, j = random.randint(0, size-1), random.randint(0, size-1)
            arr[i], arr[j] = arr[j], arr[i]
        datasets['partial'][size] = arr
    
    return series1, series2, datasets

def analyze_merge_sort():
    print("="*70)
    print("MERGE SORT EMPIRICAL ANALYSIS")
    print("="*70)
    
    ms = MergeSort()
    series1, series2, datasets = generate_datasets()
    
    # Results storage
    results = {
        'series1': {},
        'series2': {},
        'data_types': {}
    }
    
    # Initialize series1 results
    for size in series1:
        results['series1'][size] = {'time': 0, 'comparisons': 0, 'merges': 0}
    
    # Initialize series2 results
    for size in series2:
        results['series2'][size] = {'time': 0, 'comparisons': 0, 'merges': 0}
    
    # Initialize data_types results
    for data_type in ['random', 'sorted', 'reverse', 'partial']:
        results['data_types'][data_type] = {}
        for size in series2:
            results['data_types'][data_type][size] = {'time': 0, 'comparisons': 0, 'merges': 0}
    
    # Analyze Series 1 (smaller sizes) - Random data
    print("\n" + "-"*70)
    print("SERIES 1 - Smaller Input Sizes (Random Data)")
    print("-"*70)
    print(f"{'n':<10} {'Time (s)':<15} {'Comparisons':<15} {'Merges':<15}")
    print("-"*70)
    
    for size in series1:
        data = datasets['random'][size]
        ms.sort(data)
        results['series1'][size]['time'] = ms.execution_time
        results['series1'][size]['comparisons'] = ms.comparisons
        results['series1'][size]['merges'] = ms.merges
        print(f"{size:<10} {ms.execution_time:<15.6f} {ms.comparisons:<15} {ms.merges:<15}")
    
    # Analyze Series 2 (larger sizes) - All data types
    print("\n" + "-"*70)
    print("SERIES 2 - Larger Input Sizes (All Data Types)")
    print("-"*70)
    
    for data_type in ['random', 'sorted', 'reverse', 'partial']:
        print(f"\n{data_type.upper()} DATA:")
        print(f"{'n':<10} {'Time (s)':<15} {'Comparisons':<15} {'Merges':<15}")
        print("-"*55)
        
        for size in series2:
            data = datasets[data_type][size]
            ms.sort(data)
            results['data_types'][data_type][size]['time'] = ms.execution_time
            results['data_types'][data_type][size]['comparisons'] = ms.comparisons
            results['data_types'][data_type][size]['merges'] = ms.merges
            print(f"{size:<10} {ms.execution_time:<15.6f} {ms.comparisons:<15} {ms.merges:<15}")
    
    return results, series1, series2

def plot_results(results, series1, series2):
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Plot 1: Series 1 - Time growth
    ax = axes[0, 0]
    sizes = list(results['series1'].keys())
    times = [results['series1'][s]['time'] for s in sizes]
    ax.plot(sizes, times, 'b-o', linewidth=2, markersize=8)
    ax.set_xlabel('Input Size (n)')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Merge Sort Time Complexity - Series 1', fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Plot 2: Series 1 - Comparisons growth
    ax = axes[0, 1]
    comparisons = [results['series1'][s]['comparisons'] for s in sizes]
    ax.plot(sizes, comparisons, 'r-s', linewidth=2, markersize=8)
    ax.set_xlabel('Input Size (n)')
    ax.set_ylabel('Number of Comparisons')
    ax.set_title('Merge Sort Comparisons - Series 1', fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Series 2 - Comparison of data types
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
    ax.set_title('Merge Sort - Performance by Data Type', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Theoretical vs Actual
    ax = axes[1, 1]
    n = np.array(sizes)
    
    # Get actual times for random data
    actual_times = [results['data_types']['random'][s]['time'] for s in sizes]
    
    # Normalize n log n for comparison
    n_log_n = n * np.log2(n)
    if actual_times[-1] > 0:
        n_log_n = n_log_n / n_log_n[-1] * actual_times[-1]
    
    ax.plot(sizes, actual_times, 'b-o', linewidth=2, markersize=8, label='Actual (Random)')
    ax.plot(sizes, n_log_n, 'r--', linewidth=2, label='n log n Reference')
    ax.set_xlabel('Input Size (n)')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Merge Sort - Theoretical vs Actual', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('merge_sort_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    results, series1, series2 = analyze_merge_sort()
    plot_results(results, series1, series2)