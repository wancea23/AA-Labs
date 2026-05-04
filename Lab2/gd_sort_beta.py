import numpy as np

def gradient_descent_sort(arr, lr, steps):
    original = np.array(arr, dtype=float)
    n = len(original)

    true_ranks = np.argsort(np.argsort(original)).astype(float)

    # Normalization
    x_min, x_max = original.min(), original.max()
    x_norm = (original - x_min) / (x_max - x_min)

    # Logarithmic normalization
    # assert np.all(original > 0), "All values must be positive for log normalization"
    # x_log = np.log(original)
    # x_min_l, x_max_l = x_log.min(), x_log.max()
    # x_norm = (x_log - x_min_l) / (x_max_l - x_min_l)

    print("=" * 90)
    print(f"INPUT:        {original.astype(int).tolist()}")
    print(f"TRUE RANKS:   {true_ranks.astype(int).tolist()}")
    print(f"NORMALIZED:   {x_norm.tolist()}")
    print("=" * 90)
    print()
    print(f"{'Iter':<8} {'w':>12} {'b':>12} {'MSE':>12}   {'Predicted ranks'}")
    print("-" * 90)

    w = 0.0
    b = 0.0

    for step in range(1, steps + 1):
        predicted = w * x_norm + b
        error = predicted - true_ranks
        loss = np.mean(error ** 2)

        dw = (2 / n) * np.dot(error, x_norm)
        db = (2 / n) * np.sum(error)

        pred_r = [round(float(p), 2) for p in predicted]
        print(f"{step:<8} {w:>12.6f} {b:>12.6f} {loss:>12.6f}   {pred_r}")

        if loss < 0.001:
            print(f"\nConverged at step {step}!")
            break

        w -= lr * dw
        b -= lr * db

    print()
    print("=" * 90)
    print("FINAL RESULT")
    print("=" * 90)
    predicted_final = w * x_norm + b
    print(f"  w   = {w:.8f}")
    print(f"  b   = {b:.8f}")
    print(f"  MSE = {np.mean((predicted_final - true_ranks) ** 2):.8f}")
    print()
    print(f"  {'Value':>20}  {'Normalized':>10}  {'Score':>8}  {'Pred Rank':>10}  {'True Rank':>10}")
    print(f"  {'-'*75}")
    order = np.argsort(predicted_final).tolist()
    for i in range(n):
        print(f"  {original[i]:>20f}  {x_norm[i]:>10.4f}  {predicted_final[i]:>8.4f}  {order.index(i):>10}  {int(true_ranks[i]):>10}")
    print()
    result = original[np.argsort(predicted_final)].tolist()
    correct = np.sort(original).astype(float).tolist()
    print(f"  Sorted result:  {result}")
    print(f"  Correct answer: {correct}")
    print(f"  Match: {result == correct}")

gradient_descent_sort(
    [45, 3278, 12390, 0.0001, 0.0002, 0.000001,0.0000000000001,0.00000000000011,0.000002,0.5,2, 3, 99, 3232, 51515, 200000000009],
    lr=0.1,
    steps=10
)