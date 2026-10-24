# Writes data/jobs.txt: the graphs and the queries that oracle.py runs
# through networkx and mini_networkx.kara runs through the port.
import os

state = [0x2545F491]


def rnd(n):
    # xorshift32
    x = state[0]
    x ^= (x << 13) & 0xFFFFFFFF
    x ^= x >> 17
    x ^= (x << 5) & 0xFFFFFFFF
    state[0] = x & 0xFFFFFFFF
    return state[0] % n


def isqrt(n):
    x = 0
    while (x + 1) * (x + 1) <= n:
        x += 1
    return x


out = []


def emit(s):
    out.append(s)


SYL = ["ash", "bar", "cal", "dun", "elm", "fen", "gar", "hol", "ing", "kel",
       "lin", "mor", "nor", "oak", "pen", "ros", "sal", "tor", "ul", "ven",
       "wes", "yar"]
END = ["by", "ford", "ham", "ley", "mouth", "stead", "ton", "wick"]


def town_names(k):
    names = []
    seen = set()
    while len(names) < k:
        s = SYL[rnd(len(SYL))] + END[rnd(len(END))]
        if s not in seen:
            seen.add(s)
            names.append(s)
    return names


# ---------------------------------------------------------------- roads
towns = town_names(42)
pos = [(rnd(1000), rnd(1000)) for _ in towns]
edges = {}
order = []


def road(i, j, w):
    key = (min(i, j), max(i, j))
    if i == j or key in edges:
        return
    edges[key] = w
    order.append((i, j, w))


for i in range(38):
    ds = []
    for j in range(38):
        if j != i:
            dx = pos[i][0] - pos[j][0]
            dy = pos[i][1] - pos[j][1]
            ds.append((dx * dx + dy * dy, j))
    ds.sort()
    for d, j in ds[:2 + rnd(2)]:
        road(i, j, isqrt(d) // 10 + 1 + rnd(9))
# four spur towns hang off one town each (bridges, cut points)
for i in range(38, 42):
    j = rnd(38)
    road(j, i, 5 + rnd(30))
road(41, 40, 12)
emit("graph roads undirected")
for i, j, w in order:
    emit(f"e {towns[i]} {towns[j]} {w}")
emit("end")

# ---------------------------------------------------------------- deps
LIBS = ["core", "util", "log", "io", "net", "http", "json", "yaml", "cli",
        "auth", "crypt", "db", "orm", "cache", "queue", "mail", "tmpl", "web",
        "api", "admin", "search", "geo", "img", "pdf", "test", "lint", "doc",
        "bench", "metric", "trace", "conf", "sched", "pay", "cart", "user",
        "feed", "chat", "file", "zip", "diff"]
pk = ["lib" + s for s in LIBS] + ["app" + s for s in ["shop", "blog", "wiki", "crm", "ops", "desk"]]
emit("graph deps directed")
for i, p in enumerate(pk):
    if i == 0:
        emit(f"n {p}")
        continue
    k = 1 + rnd(3) if i < len(LIBS) else 3 + rnd(4)
    lo = 0 if i < len(LIBS) else 5
    used = set()
    for _ in range(k):
        j = lo + rnd(min(i, len(LIBS)) - lo) if min(i, len(LIBS)) > lo else rnd(i)
        if j in used:
            continue
        used.add(j)
        emit(f"e {pk[j]} {p} {2 + rnd(28)}")
emit("end")

# ---------------------------------------------------------------- web
pages = ["home", "about", "blog", "shop", "help", "faq", "team", "jobs"]
pages += [f"post{i:02d}" for i in range(18)] + [f"item{i:02d}" for i in range(16)]
pages += ["cart", "login", "terms", "privacy", "contact", "press"]
emit("graph web directed")
for i, p in enumerate(pages):
    if p in ("terms", "privacy", "press"):
        continue
    k = 1 + rnd(3)
    for _ in range(k):
        j = rnd(len(pages))
        if j != i:
            emit(f"e {p} {pages[j]} 1")
emit("end")

# ---------------------------------------------------------------- pipes
layers = [["src"]]
for li in range(5):
    layers.append([f"j{li}{chr(97 + k)}" for k in range(3 + rnd(3))])
layers.append(["sink"])
emit("graph pipes directed")
for li in range(len(layers) - 1):
    for u in layers[li]:
        for v in layers[li + 1]:
            if rnd(3) != 0 or len(layers[li + 1]) == 1:
                emit(f"e {u} {v} {1 + rnd(40)}")
    if 0 < li < len(layers) - 2 and len(layers[li]) > 1:
        a = layers[li][0]
        b = layers[li][1]
        emit(f"e {a} {b} {1 + rnd(15)}")
        emit(f"e {b} {a} {1 + rnd(15)}")
emit("end")

# ---------------------------------------------------------------- torus
emit("graph ring undirected")
R, C = 5, 6
for r in range(R):
    for c in range(C):
        emit(f"e r{r}c{c} r{r}c{(c + 1) % C} {1 + rnd(9)}")
        emit(f"e r{r}c{c} r{(r + 1) % R}c{c} {1 + rnd(9)}")
emit("end")

# ---------------------------------------------------------------- random
for gi in range(10):
    n = 14 + rnd(14)
    names = [f"v{k:02d}" for k in range(n)]
    kind = gi % 5
    emit(f"graph g{gi} undirected")
    for k in range(n):
        emit(f"n {names[k]}")
    if kind == 0:  # tree
        for k in range(1, n):
            emit(f"e {names[rnd(k)]} {names[k]} {1 + rnd(20)}")
    elif kind == 1:  # bipartite
        for _ in range(n + n // 2):
            a = 2 * rnd(n // 2)
            b = 2 * rnd(n // 2) + 1
            emit(f"e {names[a]} {names[b]} {1 + rnd(20)}")
    else:
        p = [12, 20, 30][kind - 2]
        for a in range(n):
            for b in range(a + 1, n):
                if rnd(100) < p:
                    emit(f"e {names[a]} {names[b]} {1 + rnd(20)}")
    emit("end")

# ---------------------------------------------------------------- queries
Q = []


def q(s):
    Q.append(s)


def pick(lst):
    return lst[rnd(len(lst))]


q("info roads")
for _ in range(14):
    a, b = pick(towns), pick(towns)
    q(f"path roads {a} {b}")
    q(f"dijkstra roads {a} {b}")
for _ in range(4):
    q(f"reach roads {pick(towns)} 10")
    q(f"bfs roads {pick(towns)}")
    q(f"dfs roads {pick(towns)}")
for op in ["components", "mst", "maxst", "cuts", "bridges", "core", "color lf",
           "color dsatur", "triangles", "bipartite", "ecc", "wdiam", "euler"]:
    q(f"{op} roads")
for _ in range(3):
    q(f"paths roads {pick(towns)} {pick(towns)} 5")
for d in [1, 3]:
    q(f"degree roads {towns[d]}")
q("copy roads closed")
for _ in range(6):
    i, j, w = order[rnd(len(order))]
    q(f"rmedge closed {towns[i]} {towns[j]}")
q(f"rmedge closed {towns[0]} nowhere")
q(f"rmnode closed {towns[5]}")
q(f"rmnode closed {towns[5]}")
q(f"addedge closed {towns[2]} {towns[30]} 4")
q(f"addedge closed {towns[5]} {towns[7]} 9")
q("info closed")
for op in ["components", "mst", "cuts", "bridges", "core", "ecc", "color lf"]:
    q(f"{op} closed")
for _ in range(8):
    a, b = pick(towns), pick(towns)
    q(f"path closed {a} {b}")
    q(f"dijkstra closed {a} {b}")
q("path closed nowhere ashby")
q("dijkstra closed ashby nowhere")

q("info deps")
for op in ["isdag", "topo", "lextopo", "generations", "longest", "reduce",
           "scc", "cycle"]:
    q(f"{op} deps")
for _ in range(6):
    q(f"ancestors deps {pick(pk)}")
    q(f"descendants deps {pick(pk)}")
for _ in range(4):
    q(f"path deps {pick(pk)} {pick(pk)}")
    q(f"dijkstra deps {pick(pk)} {pick(pk)}")
q("copy deps loop")
q("addedge loop appshop libutil 3")
q("addedge loop libdiff libcore 3")
for op in ["isdag", "topo", "scc", "cycle", "condense"]:
    q(f"{op} loop")
q("rmedge loop libdiff libcore")
q("cycle loop")

q("info web")
for op in ["scc", "condense", "cycle", "isdag"]:
    q(f"{op} web")
for _ in range(6):
    q(f"bfs web {pick(pages)}")
    q(f"dfs web {pick(pages)}")
    q(f"path web {pick(pages)} {pick(pages)}")
    q(f"descendants web {pick(pages)}")
q("components web")

q("info pipes")
q("maxflow pipes src sink")
q("longest pipes")
q("topo pipes")
q(f"maxflow pipes src {layers[3][0]}")
q(f"maxflow pipes {layers[1][0]} sink")
q("copy pipes pipes2")
q(f"rmedge pipes2 {layers[2][0]} {layers[3][0]}")
q(f"addedge pipes2 src {layers[4][1]} 25")
q("maxflow pipes2 src sink")
q("maxflow pipes2 sink src")
q("maxflow pipes2 src src")

q("info ring")
for op in ["euler", "ecc", "wdiam", "bipartite", "color lf", "color dsatur",
           "core", "triangles", "mst", "cuts", "bridges"]:
    q(f"{op} ring")
q("paths ring r0c0 r2c3 6")
q("copy ring ring2")
q("rmedge ring2 r0c0 r0c1")
q("euler ring2")
q("addedge ring2 r0c0 r0c1 3")
q("euler ring2")

for gi in range(10):
    g = f"g{gi}"
    q(f"info {g}")
    for op in ["components", "cuts", "bridges", "core", "color lf",
               "color dsatur", "triangles", "bipartite", "ecc", "mst", "euler",
               "cycle"]:
        q(f"{op} {g}")
    q(f"bfs {g} v00")
    q(f"dfs {g} v01")
    q(f"paths {g} v00 v03 7")
    q(f"reach {g} v02 6")

for s in Q:
    emit("q " + s)

os.makedirs("data", exist_ok=True)
with open("data/jobs.txt", "w", newline="\n") as f:
    f.write("\n".join(out) + "\n")
print(len(out), "lines", len(Q), "queries")
