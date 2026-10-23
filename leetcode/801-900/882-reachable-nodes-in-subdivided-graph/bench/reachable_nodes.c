// LeetCode #882 bench: C mirror of reachable_nodes.kara (the ★ arm,
// Dijkstra with a priority queue) on the same 600 graphs. C has no
// priority queue, so a binary min-heap of (distance, node) pairs is
// written out here.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t d, u; } Entry;

static Entry *heap;
static int64_t heap_len;

static int less(Entry a, Entry b) {
    return a.d < b.d || (a.d == b.d && a.u < b.u);
}

static void heap_push(Entry x) {
    int64_t i = heap_len++;
    heap[i] = x;
    while (i > 0 && less(heap[i], heap[(i - 1) / 2])) {
        Entry t = heap[i]; heap[i] = heap[(i - 1) / 2]; heap[(i - 1) / 2] = t;
        i = (i - 1) / 2;
    }
}

static Entry heap_pop(void) {
    Entry top = heap[0];
    heap[0] = heap[--heap_len];
    int64_t i = 0;
    for (;;) {
        int64_t least = i, l = 2 * i + 1, r = 2 * i + 2;
        if (l < heap_len && less(heap[l], heap[least])) least = l;
        if (r < heap_len && less(heap[r], heap[least])) least = r;
        if (least == i) break;
        Entry t = heap[i]; heap[i] = heap[least]; heap[least] = t;
        i = least;
    }
    return top;
}

// edges[3 * e], edges[3 * e + 1], edges[3 * e + 2]: u, v, cnt
static int64_t reachable_nodes(const int64_t *edges, int64_t m, int64_t max_moves, int64_t n) {
    int64_t *degree = calloc((size_t)n + 1, sizeof *degree);
    for (int64_t e = 0; e < m; e++) {
        degree[edges[3 * e] + 1]++;
        degree[edges[3 * e + 1] + 1]++;
    }
    for (int64_t u = 0; u < n; u++) degree[u + 1] += degree[u];
    int64_t *adj = malloc((size_t)(2 * m + 1) * sizeof *adj);
    int64_t *fill = malloc((size_t)n * sizeof *fill);
    for (int64_t u = 0; u < n; u++) fill[u] = degree[u];
    for (int64_t e = 0; e < m; e++) {
        adj[fill[edges[3 * e]]++] = e;
        adj[fill[edges[3 * e + 1]]++] = e;
    }
    int64_t *dist = malloc((size_t)n * sizeof *dist);
    for (int64_t u = 0; u < n; u++) dist[u] = max_moves + 1;
    dist[0] = 0;
    heap = malloc((size_t)(2 * m + 2) * sizeof *heap);
    heap_len = 0;
    heap_push((Entry){0, 0});
    while (heap_len > 0) {
        Entry top = heap_pop();
        int64_t d = top.d, u = top.u;
        if (d > dist[u]) continue;
        for (int64_t k = degree[u]; k < degree[u + 1]; k++) {
            int64_t e = adj[k];
            int64_t v = edges[3 * e] + edges[3 * e + 1] - u;
            int64_t next = d + edges[3 * e + 2] + 1;
            if (next < dist[v]) {
                dist[v] = next;
                heap_push((Entry){next, v});
            }
        }
    }
    int64_t seen = 0;
    for (int64_t u = 0; u < n; u++) if (dist[u] <= max_moves) seen++;
    for (int64_t e = 0; e < m; e++) {
        int64_t a = max_moves - dist[edges[3 * e]], b = max_moves - dist[edges[3 * e + 1]];
        if (a < 0) a = 0;
        if (b < 0) b = 0;
        seen += a + b < edges[3 * e + 2] ? a + b : edges[3 * e + 2];
    }
    free(degree); free(adj); free(fill); free(dist); free(heap);
    return seen;
}

static int64_t seed = 882;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t below(int64_t limit) {
    int64_t x = next_random();
    int64_t y = next_random();
    return (x * 32768 + y) % limit;
}

int main(void) {
    int64_t total = 0, check = 0;
    int64_t *edges = malloc(3 * 3 * 3000 * sizeof *edges);
    for (int k = 0; k < 600; k++) {
        int64_t n = 2000 + below(1001);
        int64_t offsets[3];
        int count = 0;
        while (count < 3) {
            int64_t d = 1 + below(n / 2 - 1);
            int dup = 0;
            for (int i = 0; i < count; i++) if (offsets[i] == d) dup = 1;
            if (!dup) offsets[count++] = d;
        }
        int64_t m = 0;
        for (int64_t u = 0; u < n; u++) {
            for (int j = 0; j < 3; j++) {
                edges[3 * m] = u;
                edges[3 * m + 1] = (u + offsets[j]) % n;
                edges[3 * m + 2] = below(10001);
                m++;
            }
        }
        int64_t max_moves = below(200000);
        int64_t reached = reachable_nodes(edges, m, max_moves, n);
        total += reached;
        check = (check * 131 + reached) % 1000000007;
    }
    free(edges);
    printf("600 graphs of up to 3000 nodes: %lld nodes reached, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
