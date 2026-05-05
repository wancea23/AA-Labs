import os
import sys
import time
import json
import heapq
import random
import tracemalloc
from dataclasses import dataclass


INF = float('inf')


class WeightedGraph:
    def __init__(self, n: int):
        self.V = n
        self.adj: dict[int, list[tuple[int, int]]] = {i: [] for i in range(n)}

    def add_edge(self, u: int, v: int, w: int):
        self.adj[u].append((v, w))
        self.adj[v].append((u, w))

    def to_matrix(self) -> list[list[float]]:
        dist = [[INF] * self.V for _ in range(self.V)]
        for i in range(self.V):
            dist[i][i] = 0
        for u in self.adj:
            for v, w in self.adj[u]:
                if w < dist[u][v]:
                    dist[u][v] = w
                    dist[v][u] = w
        return dist

    @staticmethod
    def random_sparse(n: int, seed: int = 42) -> "WeightedGraph":
        rng = random.Random(seed)
        g = WeightedGraph(n)
        edge_set = set()
        nodes = list(range(n))
        rng.shuffle(nodes)
        for i in range(1, n):
            u = nodes[i]
            v = nodes[rng.randint(0, i - 1)]
            key = (min(u, v), max(u, v))
            if key not in edge_set:
                edge_set.add(key)
                g.add_edge(u, v, rng.randint(1, 20))
        extras = max(0, int(n * 0.5))
        for _ in range(extras):
            u = rng.randint(0, n - 1)
            v = rng.randint(0, n - 1)
            if u != v:
                key = (min(u, v), max(u, v))
                if key not in edge_set:
                    edge_set.add(key)
                    g.add_edge(u, v, rng.randint(1, 20))
        return g

    @staticmethod
    def random_dense(n: int, seed: int = 42) -> "WeightedGraph":
        rng = random.Random(seed)
        g = WeightedGraph(n)
        for u in range(n):
            for v in range(u + 1, n):
                if rng.random() < 0.6:
                    g.add_edge(u, v, rng.randint(1, 20))
        return g


def dijkstra(graph: WeightedGraph, src: int = 0) -> list[float]:
    dist = [INF] * graph.V
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph.adj[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist


def floyd_warshall(graph: WeightedGraph) -> list[list[float]]:
    n = graph.V
    dist = graph.to_matrix()
    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue
            for j in range(n):
                nd = dist[i][k] + dist[k][j]
                if nd < dist[i][j]:
                    dist[i][j] = nd
    return dist


@dataclass
class Result:
    algorithm:      str
    graph_type:     str
    num_vertices:   int
    elapsed_ms:     float
    peak_memory_kb: float


def measure(algo_name: str, graph: WeightedGraph, graph_type: str,
            repeats: int = 5) -> Result:
    times, mems = [], []
    for _ in range(repeats):
        tracemalloc.start()
        t0 = time.perf_counter()
        if algo_name == "Dijkstra":
            dijkstra(graph, src=0)
        else:
            floyd_warshall(graph)
        elapsed = (time.perf_counter() - t0) * 1000
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        times.append(elapsed)
        mems.append(peak / 1024)
    return Result(
        algorithm      = algo_name,
        graph_type     = graph_type,
        num_vertices   = graph.V,
        elapsed_ms     = sum(times) / repeats,
        peak_memory_kb = sum(mems)  / repeats,
    )


def run_analysis():
    sparse_sizes = [10, 25, 50, 100, 250]
    dense_sizes  = [10, 25, 50, 100, 200]

    all_results: list[Result] = []

    print("=" * 68)
    print(f"{'Algorithm':<14} {'Graph Type':<16} {'N':>6}  {'Time (ms)':>12}  {'Mem (KB)':>10}")
    print("=" * 68)

    for n in sparse_sizes:
        g = WeightedGraph.random_sparse(n)
        for algo in ("Dijkstra", "Floyd-Warshall"):
            if algo == "Floyd-Warshall" and n > 500:
                continue
            r = measure(algo, g, "Sparse")
            all_results.append(r)
            print(f"{r.algorithm:<14} {r.graph_type:<16} {r.num_vertices:>6}  "
                  f"{r.elapsed_ms:>12.4f}  {r.peak_memory_kb:>10.2f}")

    for n in dense_sizes:
        g = WeightedGraph.random_dense(n)
        for algo in ("Dijkstra", "Floyd-Warshall"):
            r = measure(algo, g, "Dense")
            all_results.append(r)
            print(f"{r.algorithm:<14} {r.graph_type:<16} {r.num_vertices:>6}  "
                  f"{r.elapsed_ms:>12.4f}  {r.peak_memory_kb:>10.2f}")

    print("=" * 68)
    return all_results


def plot_results(results: list[Result]):
    try:
        import matplotlib.pyplot as plt
        import matplotlib.gridspec as gridspec
    except ImportError:
        print("matplotlib not installed — skipping charts.")
        return

    colours = {"Dijkstra": "#00c896", "Floyd-Warshall": "#f4a261"}
    graph_types = ["Sparse", "Dense"]

    fig = plt.figure(figsize=(16, 10))
    fig.suptitle("Dijkstra vs Floyd-Warshall — Empirical Analysis", fontsize=15, fontweight="bold")
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

    metrics = [
        (gs[0, 0], "elapsed_ms",     "Time (ms)",       "Sparse"),
        (gs[0, 1], "elapsed_ms",     "Time (ms)",       "Dense"),
        (gs[1, 0], "peak_memory_kb", "Peak Memory (KB)","Sparse"),
        (gs[1, 1], "peak_memory_kb", "Peak Memory (KB)","Dense"),
    ]

    for spec, metric, ylabel, gtype in metrics:
        ax = fig.add_subplot(spec)
        subset = [r for r in results if r.graph_type == gtype]
        for algo in ("Dijkstra", "Floyd-Warshall"):
            rows = sorted([r for r in subset if r.algorithm == algo],
                          key=lambda r: r.num_vertices)
            if not rows:
                continue
            ax.plot([r.num_vertices for r in rows],
                    [getattr(r, metric) for r in rows],
                    marker="o", label=algo, color=colours[algo], linewidth=2)
        ax.set_title(f"{gtype} Graph — {ylabel}", fontsize=10, fontweight="bold")
        ax.set_xlabel("Vertices (N)")
        ax.set_ylabel(ylabel)
        ax.legend()
        ax.grid(True, alpha=0.3)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lab5_charts.png")
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Chart saved → {out}")
    plt.show()


def export_json(results: list[Result], path: str = ""):
    if not path:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lab5_data.json")
    payload = [
        {
            "algorithm":       r.algorithm,
            "graph_type":      r.graph_type,
            "num_vertices":    r.num_vertices,
            "elapsed_ms":      round(r.elapsed_ms,     4),
            "peak_memory_kb":  round(r.peak_memory_kb, 2),
        }
        for r in results
    ]
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"JSON exported → {path}")


if __name__ == "__main__":
    sys.setrecursionlimit(10_000)
    results = run_analysis()
    export_json(results)
    plot_results(results)