import os
import time
import tracemalloc
import random
import collections
import sys
import json
from dataclasses import dataclass


class Graph:
    def __init__(self, num_vertices: int):
        self.V = num_vertices
        self.adj: dict[int, list[int]] = {i: [] for i in range(num_vertices)}

    def add_edge(self, u: int, v: int):
        self.adj[u].append(v)
        self.adj[v].append(u)

    @staticmethod
    def random_sparse(n: int, seed: int = 42) -> "Graph":
        rng = random.Random(seed)
        g = Graph(n)
        nodes = list(range(n))
        rng.shuffle(nodes)
        for i in range(1, n):
            u = nodes[i]
            v = nodes[rng.randint(0, i - 1)]
            g.add_edge(u, v)
        extras = max(0, int(n * 0.5))
        for _ in range(extras):
            u, v = rng.randint(0, n - 1), rng.randint(0, n - 1)
            if u != v:
                g.add_edge(u, v)
        return g

    @staticmethod
    def random_dense(n: int, seed: int = 42) -> "Graph":
        rng = random.Random(seed)
        g = Graph(n)
        for u in range(n):
            for v in range(u + 1, n):
                if rng.random() < 0.5:
                    g.add_edge(u, v)
        return g

    @staticmethod
    def binary_tree(n: int) -> "Graph":
        g = Graph(n)
        for i in range(n):
            left  = 2 * i + 1
            right = 2 * i + 2
            if left  < n: g.add_edge(i, left)
            if right < n: g.add_edge(i, right)
        return g

    @staticmethod
    def grid(rows: int, cols: int) -> "Graph":
        g = Graph(rows * cols)
        for r in range(rows):
            for c in range(cols):
                node = r * cols + c
                if c + 1 < cols: g.add_edge(node, node + 1)
                if r + 1 < rows: g.add_edge(node, node + cols)
        return g


@dataclass
class TraversalResult:
    algorithm:       str
    graph_type:      str
    num_vertices:    int
    visited_order:   list[int]
    nodes_visited:   int
    elapsed_ms:      float
    peak_memory_kb:  float
    max_stack_depth: int = 0


def dfs(graph: Graph, start: int = 0):
    visited = [False] * graph.V
    order   = []
    stack   = [start]
    max_depth = 0

    while stack:
        max_depth = max(max_depth, len(stack))
        node = stack.pop()
        if visited[node]:
            continue
        visited[node] = True
        order.append(node)
        for neighbour in reversed(graph.adj[node]):
            if not visited[neighbour]:
                stack.append(neighbour)

    return order, max_depth


def bfs(graph: Graph, start: int = 0):
    visited = [False] * graph.V
    order   = []
    queue   = collections.deque([start])
    visited[start] = True
    max_queue_size = 1

    while queue:
        max_queue_size = max(max_queue_size, len(queue))
        node = queue.popleft()
        order.append(node)
        for neighbour in graph.adj[node]:
            if not visited[neighbour]:
                visited[neighbour] = True
                queue.append(neighbour)

    return order, max_queue_size


def measure(algorithm_name: str, graph: Graph, graph_type: str,
            repeats: int = 5) -> TraversalResult:
    algo = dfs if algorithm_name == "DFS" else bfs
    times, memories, depths = [], [], []
    last_order = []

    for _ in range(repeats):
        tracemalloc.start()
        t0 = time.perf_counter()

        order, depth = algo(graph, start=0)

        elapsed = (time.perf_counter() - t0) * 1_000
        _, peak  = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        times.append(elapsed)
        memories.append(peak / 1024)
        depths.append(depth)
        last_order = order

    return TraversalResult(
        algorithm       = algorithm_name,
        graph_type      = graph_type,
        num_vertices    = graph.V,
        visited_order   = last_order,
        nodes_visited   = len(last_order),
        elapsed_ms      = sum(times)    / repeats,
        peak_memory_kb  = sum(memories) / repeats,
        max_stack_depth = int(sum(depths) / repeats),
    )


def run_analysis():
    sizes = [50, 100, 250, 500, 1_000, 2_500, 5_000]
    graph_types = {
        "Sparse Random": lambda n: Graph.random_sparse(n),
        "Dense Random":  lambda n: Graph.random_dense(n),
        "Binary Tree":   lambda n: Graph.binary_tree(n),
    }

    all_results: list[TraversalResult] = []

    print("=" * 70)
    print(f"{'Algorithm':<10} {'Graph Type':<18} {'N':>6}  "
          f"{'Time (ms)':>10}  {'Mem (KB)':>9}  {'Stack/Q':>8}  {'Visited':>8}")
    print("=" * 70)

    for gtype, factory in graph_types.items():
        for n in sizes:
            if gtype == "Dense Random" and n > 1_000:
                continue
            graph = factory(n)
            for algo in ("DFS", "BFS"):
                r = measure(algo, graph, gtype)
                all_results.append(r)
                print(f"{r.algorithm:<10} {r.graph_type:<18} {r.num_vertices:>6}  "
                      f"{r.elapsed_ms:>10.4f}  {r.peak_memory_kb:>9.2f}  "
                      f"{r.max_stack_depth:>8}  {r.nodes_visited:>8}")

    print("=" * 70)
    return all_results


def plot_results(results: list[TraversalResult]):
    try:
        import matplotlib.pyplot as plt
        import matplotlib.gridspec as gridspec
    except ImportError:
        print("\nmatplotlib not installed — skipping charts.")
        return

    graph_types = list(dict.fromkeys(r.graph_type for r in results))
    fig = plt.figure(figsize=(18, 12))
    fig.suptitle("DFS vs BFS — Empirical Analysis", fontsize=16, fontweight="bold")
    gs  = gridspec.GridSpec(2, len(graph_types), figure=fig, hspace=0.45, wspace=0.35)
    colours = {"DFS": "#e05263", "BFS": "#3d9eff"}

    for col, gtype in enumerate(graph_types):
        subset = [r for r in results if r.graph_type == gtype]

        ax_time = fig.add_subplot(gs[0, col])
        for algo in ("DFS", "BFS"):
            rows = sorted([r for r in subset if r.algorithm == algo], key=lambda r: r.num_vertices)
            ax_time.plot([r.num_vertices for r in rows], [r.elapsed_ms for r in rows],
                         marker="o", label=algo, color=colours[algo], linewidth=2)
        ax_time.set_title(gtype, fontsize=11, fontweight="bold")
        ax_time.set_xlabel("Number of Vertices")
        ax_time.set_ylabel("Time (ms)")
        ax_time.legend()
        ax_time.grid(True, alpha=0.3)

        ax_mem = fig.add_subplot(gs[1, col])
        for algo in ("DFS", "BFS"):
            rows = sorted([r for r in subset if r.algorithm == algo], key=lambda r: r.num_vertices)
            ax_mem.plot([r.num_vertices for r in rows], [r.peak_memory_kb for r in rows],
                        marker="s", label=algo, color=colours[algo], linewidth=2, linestyle="--")
        ax_mem.set_xlabel("Number of Vertices")
        ax_mem.set_ylabel("Peak Memory (KB)")
        ax_mem.legend()
        ax_mem.grid(True, alpha=0.3)

    out_png = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lab3_charts.png")
    plt.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.show()


def export_json(results: list[TraversalResult], path: str = ""):
    if not path:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lab3_data.json")
    payload = []
    for r in results:
        payload.append({
            "algorithm":       r.algorithm,
            "graph_type":      r.graph_type,
            "num_vertices":    r.num_vertices,
            "elapsed_ms":      round(r.elapsed_ms,     4),
            "peak_memory_kb":  round(r.peak_memory_kb, 2),
            "max_stack_depth": r.max_stack_depth,
            "nodes_visited":   r.nodes_visited,
        })
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)


if __name__ == "__main__":
    sys.setrecursionlimit(10_000)
    results = run_analysis()
    export_json(results)
    plot_results(results)