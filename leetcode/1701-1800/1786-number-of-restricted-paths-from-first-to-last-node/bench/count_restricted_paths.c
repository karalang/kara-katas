// LeetCode #1786: Number of Restricted Paths From First to Last Node -- the
// bench in C, mirroring count_restricted_paths.kara: Dijkstra from node n
// with a binary heap, then the paths summed in the order the nodes settled.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int64_t d; int32_t u; } Item;

static Item *heap;
static int heap_len;

static int less(Item a, Item b) { return a.d < b.d || (a.d == b.d && a.u < b.u); }

static void heap_push(Item x) {
    int i = heap_len++;
    heap[i] = x;
    while (i > 0) {
        int p = (i - 1) / 2;
        if (!less(heap[i], heap[p])) break;
        Item t = heap[i]; heap[i] = heap[p]; heap[p] = t;
        i = p;
    }
}

static Item heap_pop(void) {
    Item top = heap[0];
    heap[0] = heap[--heap_len];
    int i = 0;
    for (;;) {
        int l = 2 * i + 1, r = l + 1, m = i;
        if (l < heap_len && less(heap[l], heap[m])) m = l;
        if (r < heap_len && less(heap[r], heap[m])) m = r;
        if (m == i) break;
        Item t = heap[i]; heap[i] = heap[m]; heap[m] = t;
        i = m;
    }
    return top;
}

typedef struct { int32_t u, v, w; } Edge;

static int32_t count_restricted_paths(int32_t n, const Edge *edges, int m) {
    int *deg = calloc(n + 2, sizeof(int));
    for (int i = 0; i < m; i++) { deg[edges[i].u + 1]++; deg[edges[i].v + 1]++; }
    for (int i = 1; i <= n + 1; i++) deg[i] += deg[i - 1];
    int32_t *to = malloc(sizeof(int32_t) * 2 * m);
    int64_t *wt = malloc(sizeof(int64_t) * 2 * m);
    int *fill = malloc(sizeof(int) * (n + 1));
    memcpy(fill, deg, sizeof(int) * (n + 1));
    for (int i = 0; i < m; i++) {
        Edge e = edges[i];
        to[fill[e.u]] = e.v; wt[fill[e.u]++] = e.w;
        to[fill[e.v]] = e.u; wt[fill[e.v]++] = e.w;
    }
    int64_t *dist = malloc(sizeof(int64_t) * (n + 1));
    for (int i = 0; i <= n; i++) dist[i] = -1;
    int32_t *order = malloc(sizeof(int32_t) * (n + 1));
    int settled = 0;
    heap = malloc(sizeof(Item) * (2 * m + 2));
    heap_len = 0;
    heap_push((Item){0, n});
    while (heap_len > 0) {
        Item it = heap_pop();
        int32_t u = it.u;
        if (dist[u] != -1) continue;
        dist[u] = it.d;
        order[settled++] = u;
        for (int k = deg[u]; k < deg[u + 1]; k++)
            if (dist[to[k]] == -1) heap_push((Item){it.d + wt[k], to[k]});
    }
    int64_t *ways = calloc(n + 1, sizeof(int64_t));
    ways[n] = 1;
    for (int i = 0; i < settled; i++) {
        int32_t u = order[i];
        for (int k = deg[u]; k < deg[u + 1]; k++)
            if (dist[to[k]] < dist[u]) ways[u] = (ways[u] + ways[to[k]]) % 1000000007;
    }
    int32_t answer = (int32_t)ways[1];
    free(deg); free(to); free(wt); free(fill); free(dist); free(order); free(heap); free(ways);
    return answer;
}

static int64_t seed = 1786;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

#define SLOTS 16384
static int64_t slot[SLOTS];

static int joined_insert(int64_t key) {
    uint64_t h = (uint64_t)key * 11400714819323198485ull >> 50;
    while (slot[h] != -1) {
        if (slot[h] == key) return 0;
        h = (h + 1) & (SLOTS - 1);
    }
    slot[h] = key;
    return 1;
}

static int random_graph(int64_t n, int64_t extra, Edge *edges) {
    int m = 0;
    for (int i = 0; i < SLOTS; i++) slot[i] = -1;
    for (int64_t v = 2; v <= n; v++) {
        int64_t u = 1 + next_random() % (v - 1);
        int64_t w = 1 + next_random() % 100000;
        joined_insert(u * 4096 + v);
        edges[m++] = (Edge){(int32_t)u, (int32_t)v, (int32_t)w};
    }
    for (int64_t k = 0; k < extra; k++) {
        int64_t a = 1 + next_random() % n;
        int64_t b = 1 + next_random() % n;
        int64_t u = a < b ? a : b, v = a < b ? b : a;
        if (u == v) continue;
        int64_t key = u * 4096 + v;
        int fresh = 1;
        uint64_t h = (uint64_t)key * 11400714819323198485ull >> 50;
        while (slot[h] != -1) { if (slot[h] == key) { fresh = 0; break; } h = (h + 1) & (SLOTS - 1); }
        if (!fresh) continue;
        int64_t w = 1 + next_random() % 100000;
        joined_insert(key);
        edges[m++] = (Edge){(int32_t)u, (int32_t)v, (int32_t)w};
    }
    return m;
}

int main(void) {
    Edge *graphs = malloc(sizeof(Edge) * 200 * 4000);
    int counts[200];
    for (int g = 0; g < 200; g++) counts[g] = random_graph(2000, 2001, graphs + g * 4000);
    int64_t check = 0;
    for (int64_t call = 0; call < 1000; call++) {
        int g = (int)((check + call) % 200);
        check = (check * 31 + count_restricted_paths(2000, graphs + g * 4000, counts[g])) % 1000000007;
    }
    printf("1000 calls over 200 graphs: checksum %lld\n", (long long)check);
    free(graphs);
    return 0;
}
