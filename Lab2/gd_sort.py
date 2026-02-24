import numpy as np
import time
import matplotlib.pyplot as plt
import random
from collections import Counter

class GradientDescentSort:
    def __init__(self, learning_rate=0.01, max_steps=100, convergence_threshold=0.001):
        self.learning_rate = learning_rate
        self.max_steps = max_steps
        self.convergence_threshold = convergence_threshold
        self.w = 0.0
        self.b = 0.0
        self.steps_taken = 0
        self.final_loss = 0
        self.loss_history = []
        self.execution_time = 0
        
    def sort(self, arr):
        start_time = time.perf_counter()
        
        original = np.array(arr, dtype=float)
        n = len(original)
        
        true_ranks = np.argsort(np.argsort(original)).astype(float)
        
        x_norm = self._normalize_data(original)
        
        self.w = 0.0
        self.b = 0.0
        self.loss_history = []
        
        for step in range(1, self.max_steps + 1):
            predicted = self.w * x_norm + self.b
            error = predicted - true_ranks
            loss = np.mean(error ** 2)
            self.loss_history.append(loss)
            
            if loss < self.convergence_threshold:
                self.steps_taken = step
                break
                
            dw = (2 / n) * np.dot(error, x_norm)
            db = (2 / n) * np.sum(error)
            
            self.w -= self.learning_rate * dw
            self.b -= self.learning_rate * db
        
        self.steps_taken = step
        self.final_loss = loss
        
        predicted_final = self.w * x_norm + self.b
        sorted_indices = np.argsort(predicted_final)
        sorted_result = original[sorted_indices].tolist()
        
        self.execution_time = time.perf_counter() - start_time
        
        return sorted_result
    
    def _normalize_data(self, arr):
        assert np.all(arr > 0), "All values must be positive for log normalization"
        x_log = np.log(arr)
        x_min, x_max = x_log.min(), x_log.max()
        if x_max == x_min:
            return np.zeros_like(arr)
        return (x_log - x_min) / (x_max - x_min)
    
    def get_stats(self):
        return {
            'w': self.w,
            'b': self.b,
            'steps': self.steps_taken,
            'final_loss': self.final_loss,
            'loss_history': self.loss_history,
            'time': self.execution_time
        }


class TestDataGenerator:
    @staticmethod
    def generate_random(size, min_val=1, max_val=10000):
        return [random.uniform(min_val, max_val) for _ in range(size)]
    
    @staticmethod
    def generate_sorted(size, min_val=1, max_val=10000):
        #Already sorted data
        return sorted(TestDataGenerator.generate_random(size, min_val, max_val))
    
    @staticmethod
    def generate_reverse_sorted(size, min_val=1, max_val=10000):
        #Reverse sorted data
        return sorted(TestDataGenerator.generate_random(size, min_val, max_val), reverse=True)
    
    @staticmethod
    def generate_partially_sorted(size, min_val=1, max_val=10000):
        #70% sorted, 30% random
        arr = sorted(TestDataGenerator.generate_random(size, min_val, max_val))
        shuffle_count = size // 3
        for _ in range(shuffle_count):
            i, j = random.randint(0, size-1), random.randint(0, size-1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    
    @staticmethod
    def generate_exponential_scale(size):
        return [
            10 ** random.uniform(-10, 10)  # Exponents from -10 to 10
            for _ in range(size)
        ]
    
    @staticmethod
    def generate_near_duplicates(size, unique_ratio=0.3):
        base_values = [random.uniform(1, 10) for _ in range(int(size * unique_ratio))]
        return [random.choice(base_values) + random.uniform(-0.001, 0.001) 
                for _ in range(size)]


def analyze_gradient_sort():
    
    print("="*90)
    print("GRADIENT DESCENT SORT - EMPIRICAL ANALYSIS")
    print("="*90)
    
    sizes = [10, 20, 30, 50, 100, 200, 300, 500, 1000, 2000, 3000, 5000, 10000, 20000, 30000, 50000]
    
    data_types = ['random', 'sorted', 'reverse', 'partial', 'exponential', 'duplicates']
    
    # Learning rates to test
    learning_rates = [0.001, 0.01, 0.1, 0.5]
    
    # Results storage
    results = {
        'performance': {dt: {'sizes': [], 'times': [], 'steps': [], 'loss': []} 
                        for dt in data_types},
        'learning_rates': {lr: {'sizes': [], 'times': [], 'steps': []} 
                          for lr in learning_rates},
        'loss_curves': {}
    }
    
    # Test 1
    print("\n" + "-"*90)
    print("TEST 1: Performance Across Different Data Types")
    print("-"*90)
    print(f"{'Size':<8} {'Data Type':<15} {'Time (s)':<12} {'Steps':<8} {'Final Loss':<12} {'Accuracy':<10}")
    print("-"*90)
    
    gs = GradientDescentSort(learning_rate=0.01, max_steps=500)
    
    for size in sizes:
        for dt in data_types:
            # Generate data based on type
            if dt == 'random':
                data = TestDataGenerator.generate_random(size)
            elif dt == 'sorted':
                data = TestDataGenerator.generate_sorted(size)
            elif dt == 'reverse':
                data = TestDataGenerator.generate_reverse_sorted(size)
            elif dt == 'partial':
                data = TestDataGenerator.generate_partially_sorted(size)
            elif dt == 'exponential':
                data = TestDataGenerator.generate_exponential_scale(size)
            else:  # duplicates
                data = TestDataGenerator.generate_near_duplicates(size)
            
            sorted_result = gs.sort(data)
            stats = gs.get_stats()
            
            # Calculate accuracy
            correct = sorted(data)
            accuracy = sum(1 for i, j in zip(sorted_result, correct) if abs(i-j) < 1e-6) / size
            
            # Store results
            results['performance'][dt]['sizes'].append(size)
            results['performance'][dt]['times'].append(stats['time'])
            results['performance'][dt]['steps'].append(stats['steps'])
            results['performance'][dt]['loss'].append(stats['final_loss'])
            
            print(f"{size:<8} {dt:<15} {stats['time']:<12.6f} {stats['steps']:<8} "
                  f"{stats['final_loss']:<12.6f} {accuracy:<10.2%}")
    
    # Test 2
    print("\n" + "-"*90)
    print("TEST 2: Effect of Learning Rate (Random Data, size=100)")
    print("-"*90)
    print(f"{'LR':<8} {'Time (s)':<12} {'Steps':<8} {'Final Loss':<12} {'Converged':<10}")
    print("-"*90)
    
    test_size = 100
    test_data = TestDataGenerator.generate_random(test_size)
    
    for lr in learning_rates:
        gs = GradientDescentSort(learning_rate=lr, max_steps=1000)
        sorted_result = gs.sort(test_data)
        stats = gs.get_stats()
        
        results['learning_rates'][lr]['sizes'].append(test_size)
        results['learning_rates'][lr]['times'].append(stats['time'])
        results['learning_rates'][lr]['steps'].append(stats['steps'])
        
        converged = stats['steps'] < gs.max_steps
        print(f"{lr:<8.3f} {stats['time']:<12.6f} {stats['steps']:<8} "
              f"{stats['final_loss']:<12.6f} {str(converged):<10}")
    
    # Test 3
    print("\n" + "-"*90)
    print("TEST 3: Training Loss Curves (size=200)")
    print("-"*90)
    
    for dt in ['random', 'sorted', 'exponential']:
        if dt == 'random':
            data = TestDataGenerator.generate_random(200)
        elif dt == 'sorted':
            data = TestDataGenerator.generate_sorted(200)
        else:
            data = TestDataGenerator.generate_exponential_scale(200)
        
        gs = GradientDescentSort(learning_rate=0.01, max_steps=200)
        sorted_result = gs.sort(data)
        results['loss_curves'][dt] = gs.get_stats()['loss_history']
    
    return results


def plot_results(results):
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    # Plot 1: Time comparison across data types
    ax = axes[0, 0]
    colors = {'random': 'blue', 'sorted': 'green', 'reverse': 'red', 
              'partial': 'orange', 'exponential': 'purple', 'duplicates': 'brown'}
    
    for dt, data in results['performance'].items():
        ax.plot(data['sizes'], data['times'], 'o-', color=colors.get(dt, 'gray'), 
                linewidth=2, markersize=6, label=dt.capitalize())
    
    ax.set_xlabel('Input Size')
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Gradient Sort - Time by Data Type', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 2: Steps to convergence
    ax = axes[0, 1]
    for dt, data in results['performance'].items():
        ax.plot(data['sizes'], data['steps'], 'o-', color=colors.get(dt, 'gray'),
                linewidth=2, markersize=6, label=dt.capitalize())
    
    ax.set_xlabel('Input Size')
    ax.set_ylabel('Steps to Convergence')
    ax.set_title('Gradient Sort - Convergence Speed', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Final loss
    ax = axes[0, 2]
    for dt, data in results['performance'].items():
        ax.plot(data['sizes'], data['loss'], 'o-', color=colors.get(dt, 'gray'),
                linewidth=2, markersize=6, label=dt.capitalize())
    
    ax.set_xlabel('Input Size')
    ax.set_ylabel('Final MSE Loss')
    ax.set_title('Gradient Sort - Final Loss', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')  # Log scale for loss
    
    # Plot 4: Effect of learning rate
    ax = axes[1, 0]
    lrs = []
    times = []
    steps = []
    
    for lr, data in results['learning_rates'].items():
        lrs.append(lr)
        times.append(data['times'][0])
        steps.append(data['steps'][0])
    
    ax2 = ax.twinx()
    ax.plot(lrs, times, 'b-o', linewidth=2, markersize=8, label='Time')
    ax2.plot(lrs, steps, 'r-s', linewidth=2, markersize=8, label='Steps')
    
    ax.set_xlabel('Learning Rate')
    ax.set_ylabel('Time (seconds)', color='b')
    ax2.set_ylabel('Steps to Converge', color='r')
    ax.set_title('Effect of Learning Rate (n=100)', fontweight='bold')
    ax.set_xscale('log')
    ax.grid(True, alpha=0.3)
    
    # Plot 5: Loss curves
    ax = axes[1, 1]
    for dt, loss_history in results['loss_curves'].items():
        ax.plot(loss_history, linewidth=2, label=dt.capitalize())
    
    ax.set_xlabel('Iteration')
    ax.set_ylabel('MSE Loss')
    ax.set_title('Training Loss Curves (n=200)', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')
    
    # Plot 6: Theoretical analysis
    ax = axes[1, 2]
    
    # Complexity comparison with traditional sorts
    sizes = np.array([10, 50, 100, 500, 1000])
    n_log_n = sizes * np.log2(sizes)
    n_squared = sizes ** 2
    
    # Normalize for comparison
    gd_times = results['performance']['random']['times'][:len(sizes)]
    gd_times = np.array(gd_times) / gd_times[-1] if gd_times[-1] > 0 else gd_times
    
    ax.plot(sizes, gd_times, 'b-o', linewidth=2, markersize=8, label='Gradient Sort')
    ax.plot(sizes, n_log_n / n_log_n[-1], 'r--', linewidth=2, label='O(n log n)')
    ax.plot(sizes, n_squared / n_squared[-1], 'g--', linewidth=2, label='O(n²)')
    
    ax.set_xlabel('Input Size')
    ax.set_ylabel('Normalized Time')
    ax.set_title('Complexity Comparison', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('gradient_sort_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    results = analyze_gradient_sort()
    plot_results(results)