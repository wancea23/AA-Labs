import time
import matplotlib.pyplot as plt

def lucas(n):
    if n == 0:
        return 2
    if n == 1:
        return 1

    a, b = 2, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def fibonacci_lucas(n):
    if n == 0:
        return 0
    return (lucas(n - 1) + lucas(n + 1)) // 5

def test_second_series(n_values):
    print("\n" + "="*100)
    print("RESULTS FOR LUCAS METHOD - SECOND INPUT SERIES")
    print("="*100)
    
    print("|   ", end="")
    for n in n_values:
        print(f"| {n} ", end="")
    print("|")
    
    print("| 0 ", end="")
    times = []
    
    for n in n_values:
        start = time.perf_counter()
        fibonacci_lucas(n)
        end = time.perf_counter()
        
        t = end - start
        times.append(t)
        print(f"| {t:.8f} ", end="")
    
    print("|")
    print("="*100)
    
    return n_values, times

def plot_second_series(n_values, times):
    plt.figure(figsize=(14, 7))
    plt.plot(n_values, times, 'bo-', linewidth=2, markersize=6)
    plt.xlabel("Fibonacci term (n)")
    plt.ylabel("Execution time (seconds)")
    plt.title("Fibonacci via Lucas Method - Second Input Series")
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == "__main__":
    second_series = [501, 631, 794, 1000, 1259, 1585, 1995, 2512, 3162, 3981, 5012, 6310, 7943, 10000, 12589, 15849]
    
    n_vals, times = test_second_series(second_series)
    plot_second_series(n_vals, times)