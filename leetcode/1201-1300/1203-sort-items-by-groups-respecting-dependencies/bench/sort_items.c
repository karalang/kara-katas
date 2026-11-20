// LeetCode #1203 bench, in C: the ★ arm (each item in no group given one of
// its own, then Kahn's algorithm over the groups and over the items) on
// four instances of 30000 items drawn once, then 10 rounds over the four,
// each answer folded into a checksum. Each graph's edges are kept in the
// order they are added, per node, as the other languages' lists of lists
// keep them, in one array indexed by counts.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long long seed = 1203;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct {
    long *start; /* nodes + 1 */
    long *to;
} Graph;

/* An edge list (from[k], to[k]) gathered per node, in the order given. */
static Graph gather(long nodes, const long *from, const long *to, long count) {
    Graph g;
    g.start = calloc(nodes + 1, sizeof(long));
    g.to = malloc((count ? count : 1) * sizeof(long));
    for (long k = 0; k < count; k++) g.start[from[k] + 1]++;
    for (long v = 0; v < nodes; v++) g.start[v + 1] += g.start[v];
    long *fill = malloc((nodes ? nodes : 1) * sizeof(long));
    memcpy(fill, g.start, nodes * sizeof(long));
    for (long k = 0; k < count; k++) g.to[fill[from[k]]++] = to[k];
    free(fill);
    return g;
}

/* Kahn's algorithm; the order's length, `nodes` when every node is sorted. */
static long topo_sort(long nodes, Graph g, long *order) {
    long *indegree = calloc(nodes ? nodes : 1, sizeof(long));
    for (long k = 0; k < g.start[nodes]; k++) indegree[g.to[k]]++;
    long len = 0;
    for (long v = 0; v < nodes; v++)
        if (indegree[v] == 0) order[len++] = v;
    for (long head = 0; head < len; head++) {
        long u = order[head];
        for (long k = g.start[u]; k < g.start[u + 1]; k++) {
            long v = g.to[k];
            if (--indegree[v] == 0) order[len++] = v;
        }
    }
    free(indegree);
    return len;
}

typedef struct {
    long *start; /* n + 1 */
    long *items;
} Deps;

static long sort_items(long n, long m, const long *group, Deps before, long *out) {
    long *owner = malloc(n * sizeof(long));
    long groups = m;
    for (long i = 0; i < n; i++) owner[i] = group[i] < 0 ? groups++ : group[i];
    long e = before.start[n];
    long *if_ = malloc((e ? e : 1) * sizeof(long)), *it = malloc((e ? e : 1) * sizeof(long));
    long *gf = malloc((e ? e : 1) * sizeof(long)), *gt = malloc((e ? e : 1) * sizeof(long));
    long ie = 0, ge = 0;
    for (long i = 0; i < n; i++) {
        for (long k = before.start[i]; k < before.start[i + 1]; k++) {
            long b = before.items[k];
            if_[ie] = b;
            it[ie++] = i;
            if (owner[b] != owner[i]) {
                gf[ge] = owner[b];
                gt[ge++] = owner[i];
            }
        }
    }
    Graph items_g = gather(n, if_, it, ie), groups_g = gather(groups, gf, gt, ge);
    long *items = malloc(n * sizeof(long)), *ranks = malloc(groups * sizeof(long));
    long len = 0;
    if (topo_sort(n, items_g, items) == n && topo_sort(groups, groups_g, ranks) == groups) {
        /* the items dealt into their groups, in their sorted order */
        long *mf = malloc(n * sizeof(long));
        for (long k = 0; k < n; k++) mf[k] = owner[items[k]];
        Graph members = gather(groups, mf, items, n);
        for (long r = 0; r < groups; r++) {
            long g = ranks[r];
            for (long k = members.start[g]; k < members.start[g + 1]; k++) out[len++] = members.to[k];
        }
        free(mf);
        free(members.start);
        free(members.to);
    }
    free(owner);
    free(if_);
    free(it);
    free(gf);
    free(gt);
    free(items_g.start);
    free(items_g.to);
    free(groups_g.start);
    free(groups_g.to);
    free(items);
    free(ranks);
    return len;
}

/* Up to `most` distinct earlier items for each item, as the others draw them. */
static Deps dependencies(long n, long most) {
    long cap = n * most + 2;
    long *from = malloc(cap * sizeof(long)), *to = malloc(cap * sizeof(long));
    long *pick = malloc(most * sizeof(long) + sizeof(long));
    long e = 0;
    for (long i = 1; i < n; i++) {
        long k = next_random() % (most + 1);
        long got = 0;
        for (long t = 0; t < k; t++) {
            long long hi = next_random();
            long b = (long)((hi * 32768 + next_random()) % i);
            int seen = 0;
            for (long q = 0; q < got; q++) seen |= pick[q] == b;
            if (!seen) {
                pick[got++] = b;
                from[e] = i;
                to[e++] = b;
            }
        }
    }
    free(pick);
    Graph g = gather(n, from, to, e);
    free(from);
    free(to);
    Deps d = {g.start, g.to};
    return d;
}

/* A copy of `d` with `b` added to `i`'s dependencies, at the end. */
static Deps with_dependency(long n, Deps d, long i, long b) {
    long e = d.start[n];
    Deps c;
    c.start = malloc((n + 1) * sizeof(long));
    c.items = malloc((e + 1) * sizeof(long));
    long w = 0;
    for (long v = 0; v < n; v++) {
        c.start[v] = w;
        for (long k = d.start[v]; k < d.start[v + 1]; k++) c.items[w++] = d.items[k];
        if (v == i) c.items[w++] = b;
    }
    c.start[n] = w;
    return c;
}

static int depends(Deps d, long i, long b) {
    for (long k = d.start[i]; k < d.start[i + 1]; k++)
        if (d.items[k] == b) return 1;
    return 0;
}

int main(void) {
    long n = 30000, m = 3000;
    long *runs = malloc(n * sizeof(long)), *none = malloc(n * sizeof(long));
    for (long i = 0; i < n; i++) {
        runs[i] = i % 10 == 0 ? -1 : i / 10;
        none[i] = -1;
    }
    Deps loose = dependencies(n, 3);
    Deps dense = dependencies(n, 6);
    Deps cycle = with_dependency(n, loose, 0, n - 1);
    if (!depends(cycle, n - 1, 0)) {
        Deps c2 = with_dependency(n, cycle, n - 1, 0);
        free(cycle.start);
        free(cycle.items);
        cycle = c2;
    }
    Deps third = dependencies(n, 3);
    const long *groups[4] = {runs, runs, none, runs};
    Deps deps[4] = {loose, dense, third, cycle};
    long *out = malloc(n * sizeof(long));
    long long check = 0;
    for (int round = 0; round < 10; round++) {
        for (int k = 0; k < 4; k++) {
            long len = sort_items(n, m, groups[k], deps[k], out);
            check = (check * 131 + len) % 1000000007;
            for (long i = 0; i < len; i++) check = (check * 131 + out[i] + 1) % 1000000007;
        }
    }
    printf("10 rounds over 4 instances of 30000 items: checksum %lld\n", check);
    return 0;
}
