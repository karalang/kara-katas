# Runs data/jobs.txt through networkx 3.4.2 itself; its output is
# expected.out. Run as: python3 -I -B oracle.py > expected.out, with
# networkx installed or NETWORKX_SRC naming an unpacked sdist.
import os
import sys

if os.environ.get("NETWORKX_SRC"):
    sys.path.insert(0, os.environ["NETWORKX_SRC"])
import networkx as nx  # noqa: E402
from networkx.algorithms import bipartite  # noqa: E402
from networkx.algorithms.flow import edmonds_karp  # noqa: E402

assert nx.__version__ == "3.4.2"


def fnv(s):
    h = 2166136261
    for b in s.encode("utf-8"):
        h = ((h ^ b) * 16777619) & 0xFFFFFFFF
    return f"{h:08x}"


def seq(names, k=12):
    head = " ".join(names[:k])
    more = " ..." if len(names) > k else ""
    return f"{len(names)} nodes: {head}{more}; fnv {fnv(' '.join(names))}"


def chain(p):
    return " > ".join(p)


def few(names, k):
    s = " ".join(names[:k])
    return s + (" ..." if len(names) > k else "")


def sep(G):
    return ">" if G.is_directed() else "-"


def comps_line(cs):
    parts = [f"{len(c)} {min(c)}" for c in cs]
    head = " | ".join(parts[:6]) + (" ..." if len(parts) > 6 else "")
    flat = ";".join(" ".join(sorted(c)) for c in cs)
    return f"{len(cs)} components: {head}; fnv {fnv(flat)}"


def edges_line(G, es, k):
    s = sep(G)
    return " ".join(f"{u}{s}{v}" for u, v in es[:k]) + (" ..." if len(es) > k else "")


def run(G, graphs, name, op, args):
    if op == "info":
        kind = "directed" if G.is_directed() else "undirected"
        return f"{G.number_of_nodes()} nodes, {G.number_of_edges()} edges, {kind}"
    if op == "degree":
        return f"{G.degree(args[0])}"
    if op == "path":
        p = nx.shortest_path(G, args[0], args[1])
        return f"{len(p) - 1} hops: {chain(p)}"
    if op == "dijkstra":
        d, p = nx.single_source_dijkstra(G, args[0], args[1])
        return f"dist {d}: {chain(p)}"
    if op == "reach":
        k = int(args[1])
        dist = nx.single_source_dijkstra_path_length(G, args[0])
        items = list(dist.items())
        head = ", ".join(f"{v} {d}" for v, d in items[:k])
        flat = ",".join(f"{v}:{d}" for v, d in items)
        return f"{len(items)} reached; {head}; fnv {fnv(flat)}"
    if op == "bfs":
        return seq([args[0]] + [v for u, v in nx.bfs_edges(G, args[0])])
    if op == "dfs":
        return seq([args[0]] + [v for u, v in nx.dfs_edges(G, args[0])])
    if op == "components":
        return comps_line(list(nx.connected_components(G)))
    if op == "scc":
        return comps_line(list(nx.strongly_connected_components(G)))
    if op == "condense":
        C = nx.condensation(G)
        src = sum(1 for v in C if C.in_degree(v) == 0)
        snk = sum(1 for v in C if C.out_degree(v) == 0)
        return f"{C.number_of_nodes()} nodes, {C.number_of_edges()} edges; {src} sources, {snk} sinks"
    if op in ("mst", "maxst"):
        if op == "mst":
            es = list(nx.minimum_spanning_edges(G, algorithm="kruskal", data=True))
        else:
            es = list(nx.maximum_spanning_edges(G, algorithm="kruskal", data=True))
        total = sum(d["weight"] for u, v, d in es)
        head = " ".join(f"{u}-{v} {d['weight']}" for u, v, d in es[:6])
        flat = ",".join(f"{u}-{v}:{d['weight']}" for u, v, d in es)
        return f"{len(es)} edges, weight {total}; {head} ...; fnv {fnv(flat)}"
    if op == "cuts":
        ps = list(nx.articulation_points(G))
        return f"{len(ps)} cut points: {few(ps, 12)}"
    if op == "bridges":
        bs = list(nx.bridges(G))
        return f"{len(bs)} bridges: {edges_line(G, bs, 10)}"
    if op == "core":
        cn = nx.core_number(G)
        top = max(cn.values())
        members = sorted(v for v in cn if cn[v] == top)
        hist = {}
        for v in G:
            hist[cn[v]] = hist.get(cn[v], 0) + 1
        hs = " ".join(f"{k}:{hist[k]}" for k in sorted(hist))
        return f"max core {top}: {len(members)} nodes ({few(members, 8)}); histogram {hs}"
    if op == "color":
        strat = {"lf": "largest_first", "dsatur": "saturation_largest_first"}[args[0]]
        col = nx.greedy_color(G, strategy=strat)
        k = max(col.values()) + 1 if col else 0
        sizes = [0] * k
        for v in col:
            sizes[col[v]] += 1
        flat = ",".join(f"{v}={c}" for v, c in col.items())
        return f"{k} colors, classes {' '.join(str(s) for s in sizes)}; fnv {fnv(flat)}"
    if op == "triangles":
        t = nx.triangles(G)
        total = sum(t.values()) // 3
        top = sorted(G, key=lambda v: -t[v])[:3]
        return f"{total} triangles; most at " + ", ".join(f"{v} {t[v]}" for v in top)
    if op == "bipartite":
        if not nx.is_bipartite(G):
            return "not bipartite"
        c = bipartite.color(G)
        ones = sorted(v for v in c if c[v] == 1)
        zeros = sorted(v for v in c if c[v] == 0)
        return f"bipartite, {len(ones)} + {len(zeros)}; one side {few(ones, 5)}"
    if op in ("ecc", "wdiam"):
        e = nx.eccentricity(G, weight=("weight" if op == "wdiam" else None))
        d = max(e.values())
        r = min(e.values())
        center = [v for v in e if e[v] == r]
        per = [v for v in e if e[v] == d]
        return f"diameter {d}, radius {r}, center {few(center, 6)}, periphery {len(per)}"
    if op == "euler":
        if not nx.is_eulerian(G):
            return "not eulerian"
        circ = list(nx.eulerian_circuit(G))
        nodes = [circ[0][0]] + [v for u, v in circ]
        return f"circuit of {len(circ)} edges, " + seq(nodes, 10)
    if op == "paths":
        ps = list(nx.all_simple_paths(G, args[0], args[1], cutoff=int(args[2])))
        if not ps:
            return "0 paths"
        short = min(len(p) for p in ps) - 1
        return f"{len(ps)} paths, shortest {short} hops; first {chain(ps[0])}"
    if op == "isdag":
        return "yes" if nx.is_directed_acyclic_graph(G) else "no"
    if op == "topo":
        return seq(list(nx.topological_sort(G)))
    if op == "lextopo":
        return seq(list(nx.lexicographical_topological_sort(G)))
    if op == "generations":
        gens = list(nx.topological_generations(G))
        return f"{len(gens)} generations, sizes {' '.join(str(len(g)) for g in gens)}; first {few(gens[0], 6)}"
    if op == "longest":
        p = nx.dag_longest_path(G)
        return f"length {nx.dag_longest_path_length(G)}: {chain(p)}"
    if op == "reduce":
        TR = nx.transitive_reduction(G)
        gone = [(u, v) for u, v in G.edges() if not TR.has_edge(u, v)]
        return f"{TR.number_of_edges()} kept, {len(gone)} removed: {edges_line(G, gone, 6)}"
    if op in ("ancestors", "descendants"):
        f = nx.ancestors if op == "ancestors" else nx.descendants
        s = sorted(f(G, args[0]))
        return f"{len(s)}: {few(s, 10)}"
    if op == "cycle":
        es = nx.find_cycle(G)
        nodes = [u for u, v in es] + [es[-1][1]]
        return f"cycle of {len(es)}: {chain(nodes)}"
    if op == "maxflow":
        v, (S, T) = nx.minimum_cut(G, args[0], args[1], capacity="weight", flow_func=edmonds_karp)
        cut = sorted((u, w) for u in S for w in G[u] if w in T)
        return f"value {v}; sink side {len(T)}; cut {edges_line(G, cut, 8)}"
    if op == "copy":
        H = G.copy()
        graphs[args[0]] = H
        return f"{H.number_of_nodes()} nodes, {H.number_of_edges()} edges"
    if op == "rmedge":
        G.remove_edge(args[0], args[1])
        return f"{G.number_of_nodes()} nodes, {G.number_of_edges()} edges"
    if op == "rmnode":
        G.remove_node(args[0])
        return f"{G.number_of_nodes()} nodes, {G.number_of_edges()} edges"
    if op == "addedge":
        G.add_edge(args[0], args[1], weight=int(args[2]))
        return f"{G.number_of_nodes()} nodes, {G.number_of_edges()} edges"
    raise SystemExit("unknown op " + op)


def main():
    graphs = {}
    cur = None
    for line in open("data/jobs.txt", encoding="utf-8", newline="\n").read().split("\n"):
        if not line:
            continue
        w = line.split(" ")
        if w[0] == "graph":
            cur = nx.DiGraph() if w[2] == "directed" else nx.Graph()
            graphs[w[1]] = cur
        elif w[0] == "n":
            cur.add_node(w[1])
        elif w[0] == "e":
            cur.add_edge(w[1], w[2], weight=int(w[3]))
        elif w[0] == "end":
            cur = None
        elif w[0] == "q":
            op, name, args = w[1], w[2], w[3:]
            if op == "color":
                name, args = w[3], [w[2]]
            text = " ".join(w[1:])
            try:
                res = run(graphs[name], graphs, name, op, args)
            except nx.NetworkXException as e:
                res = f"error: {e}"
            print(f"{text}: {res}")
    print(f"{len(graphs)} graphs")


main()
