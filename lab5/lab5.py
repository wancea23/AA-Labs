import time
import random
import heapq

class DSU:
    """Disjoint Set Union with path compression + union by rank."""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank   = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False                                   # already in same set
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px]  += 1
        return True

def prim(n: int, edges: list[tuple]) -> tuple[list, int]:
    # Build adjacency list
    adj: list[list] = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    in_mst  = [False] * n
    key     = [float('inf')] * n
    parent  = [-1] * n
    key[0]  = 0

    mst_edges = []

    for _ in range(n):
        # Greedy pick: minimum key vertex not yet in MST
        u = min((v for v in range(n) if not in_mst[v]), key=lambda v: key[v])
        in_mst[u] = True

        if parent[u] != -1:
            mst_edges.append((parent[u], u, key[u]))

        # Relax neighbours
        for v, w in adj[u]:
            if not in_mst[v] and w < key[v]:
                key[v]    = w
                parent[v] = u

    total = sum(w for _, _, w in mst_edges)
    return mst_edges, total


def prim_heap(n: int, edges: list[tuple]) -> tuple[list, int]:
    adj: list[list] = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    in_mst  = [False] * n
    parent  = [-1] * n
    heap    = [(0, 0)]       # (cost, vertex)
    cost    = [float('inf')] * n
    cost[0] = 0
    mst_edges = []

    while heap:
        d, u = heapq.heappop(heap)
        if in_mst[u]:
            continue
        in_mst[u] = True
        if parent[u] != -1:
            mst_edges.append((parent[u], u, d))
        for v, w in adj[u]:
            if not in_mst[v] and w < cost[v]:
                cost[v]   = w
                parent[v] = u
                heapq.heappush(heap, (w, v))

    total = sum(w for _, _, w in mst_edges)
    return mst_edges, total

def kruskal(n: int, edges: list[tuple]) -> tuple[list, int]:
    sorted_edges = sorted(edges, key=lambda e: e[2])   # sort by weight
    dsu          = DSU(n)
    mst_edges    = []

    for u, v, w in sorted_edges:
        if dsu.union(u, v):          # no cycle - add to MST
            mst_edges.append((u, v, w))
            if len(mst_edges) == n - 1:
                break                # MST is complete

    total = sum(w for _, _, w in mst_edges)
    return mst_edges, total

def make_sample_graph() -> tuple[int, list]:
    n = 8
    edges = [
        (0,1,4),(0,2,6),(1,2,6),(1,3,3),
        (2,4,2),(3,4,4),(3,5,5),(4,5,7),
        (4,6,5),(5,6,2),(5,7,6),(6,7,4),
    ]
    return n, edges


def make_random_connected_graph(n: int, density: float = 1.5) -> tuple[int, list]:
    perm = list(range(n))
    random.shuffle(perm)

    edges: list[tuple] = []
    edge_set: set = set()

    # Random spanning tree
    for i in range(1, n):
        j   = random.randrange(i)
        u, v = perm[i], perm[j]
        w   = random.randint(1, 99)
        edges.append((u, v, w))
        edge_set.add((min(u,v), max(u,v)))

    # Extra edges
    for _ in range(int(n * density)):
        u = random.randrange(n)
        v = random.randrange(n)
        key = (min(u,v), max(u,v))
        if u != v and key not in edge_set:
            edges.append((u, v, random.randint(1, 99)))
            edge_set.add(key)

    return n, edges

def benchmark(n: int, edges: list, runs: int = 10) -> dict:
    prim_total = kruskal_total = 0.0

    for _ in range(runs):
        t0 = time.perf_counter()
        prim(n, edges)
        prim_total += (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        kruskal(n, edges)
        kruskal_total += (time.perf_counter() - t0) * 1000

    return {
        "n":       n,
        "edges":   len(edges),
        "prim":    prim_total   / runs,
        "kruskal": kruskal_total / runs,
    }


def run_empirical_analysis() -> list[dict]:
    sizes  = [5, 10, 20, 50, 100, 200, 500, 1000]
    results = []
    print(f"\n{'─'*66}")
    print(f"  {'V':>6}  {'E':>6}  {'Prim (ms)':>14}  {'Kruskal (ms)':>14}  {'Faster':>10}")
    print(f"{'─'*66}")

    for n in sizes:
        runs = 20 if n <= 200 else 5
        _, edges = make_random_connected_graph(n)
        r = benchmark(n, edges, runs=runs)
        results.append(r)
        faster = "Prim" if r["prim"] < r["kruskal"] else "Kruskal"
        print(f"  {r['n']:>6}  {r['edges']:>6}  {r['prim']:>14.5f}  {r['kruskal']:>14.5f}  {faster:>10}")

    print(f"{'─'*66}\n")
    return results

LABELS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def label(i: int) -> str:
    return LABELS[i] if i < len(LABELS) else str(i)

def print_mst(name: str, mst_edges: list, total: int):
    print(f"\n  ── {name} ──")
    for u, v, w in sorted(mst_edges):
        print(f"     {label(u)} ─── {label(v)}   weight = {w}")
    print(f"     Total MST weight: {total}")




def main():
    n, edges = make_sample_graph()
    print(f"\n[SAMPLE GRAPH]  V={n}  E={len(edges)}")
    print("  Edges:", [(f"{label(u)}-{label(v)}", w) for u,v,w in edges])

    prim_mst,    prim_total    = prim(n, edges)
    kruskal_mst, kruskal_total = kruskal(n, edges)

    print("\n[MST RESULTS]")
    print_mst("Prim's    (naive O(V²))", prim_mst, prim_total)
    print_mst("Kruskal's (O(E log E))", kruskal_mst, kruskal_total)

    run_empirical_analysis()

if __name__ == "__main__":
    main()