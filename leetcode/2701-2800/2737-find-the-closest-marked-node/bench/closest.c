// LeetCode #2737: Find the Closest Marked Node -- the bench (closest.kara
// in C): Dijkstra from s with a hand-written binary heap of (distance,
// node), stopping at the first marked node taken off it. The edges are
// kept as an adjacency array built by counting.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t d, u; } Entry;

static Entry *heap;
static int64_t heap_size;

static int less(Entry a, Entry b) { return a.d < b.d || (a.d == b.d && a.u < b.u); }

static void heap_push(Entry e) {
    int64_t i = heap_size++;
    heap[i] = e;
    while (i > 0 && less(heap[i], heap[(i - 1) / 2])) {
        Entry t = heap[i]; heap[i] = heap[(i - 1) / 2]; heap[(i - 1) / 2] = t;
        i = (i - 1) / 2;
    }
}

static Entry heap_pop(void) {
    Entry top = heap[0];
    heap[0] = heap[--heap_size];
    int64_t i = 0;
    for (;;) {
        int64_t l = 2 * i + 1, r = l + 1, m = i;
        if (l < heap_size && less(heap[l], heap[m])) m = l;
        if (r < heap_size && less(heap[r], heap[m])) m = r;
        if (m == i) break;
        Entry t = heap[i]; heap[i] = heap[m]; heap[m] = t;
        i = m;
    }
    return top;
}

static int64_t minimum_distance(int64_t n, const int64_t *edges, int64_t m, int64_t s, const int64_t *marked, int64_t k) {
    int64_t *start = calloc((size_t)n + 1, sizeof(int64_t));
    int64_t *to = malloc(sizeof(int64_t) * m), *weight = malloc(sizeof(int64_t) * m);
    for (int64_t i = 0; i < m; i++) start[edges[3 * i] + 1]++;
    for (int64_t v = 0; v < n; v++) start[v + 1] += start[v];
    int64_t *fill = malloc(sizeof(int64_t) * n);
    for (int64_t v = 0; v < n; v++) fill[v] = start[v];
    for (int64_t i = 0; i < m; i++) {
        int64_t p = fill[edges[3 * i]]++;
        to[p] = edges[3 * i + 1];
        weight[p] = edges[3 * i + 2];
    }
    char *is_marked = calloc((size_t)n, 1);
    for (int64_t i = 0; i < k; i++) is_marked[marked[i]] = 1;
    int64_t *dist = malloc(sizeof(int64_t) * n);
    for (int64_t v = 0; v < n; v++) dist[v] = INT64_MAX;
    heap = malloc(sizeof(Entry) * (m + 1));
    heap_size = 0;
    dist[s] = 0;
    heap_push((Entry){0, s});
    int64_t answer = -1;
    while (heap_size > 0) {
        Entry e = heap_pop();
        if (e.d > dist[e.u]) continue;
        if (is_marked[e.u]) {
            answer = e.d;
            break;
        }
        for (int64_t p = start[e.u]; p < start[e.u + 1]; p++) {
            int64_t v = to[p], nd = e.d + weight[p];
            if (nd < dist[v]) {
                dist[v] = nd;
                heap_push((Entry){nd, v});
            }
        }
    }
    free(start); free(to); free(weight); free(fill); free(is_marked); free(dist); free(heap);
    return answer;
}

static int64_t seed = 2737;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int graphs = 50, rounds = 20;
    const int64_t n = 500, m = 10000;
    int64_t *edges = malloc(sizeof(int64_t) * 3 * m * graphs);
    int64_t starts[50], marked[50][3], counts[50];
    for (int g = 0; g < graphs; g++) {
        int64_t *e = edges + 3 * m * g;
        for (int64_t i = 0; i < m; i++) {
            int64_t u = next_random() % n;
            int64_t v = (u + 1 + next_random() % (n - 1)) % n;
            int64_t hi = next_random();
            int64_t w = (hi * 32768 + next_random()) % 1000000 + 1;
            e[3 * i] = u; e[3 * i + 1] = v; e[3 * i + 2] = w;
        }
        int64_t s = next_random() % n;
        int64_t want = next_random() % 3 + 1, have = 0;
        while (have < want) {
            int64_t v = next_random() % n;
            int seen = 0;
            for (int64_t j = 0; j < have; j++) if (marked[g][j] == v) seen = 1;
            if (v != s && !seen) marked[g][have++] = v;
        }
        starts[g] = s;
        counts[g] = have;
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int g = 0; g < graphs; g++) {
            int64_t distance = minimum_distance(n, edges + 3 * m * g, m, starts[g], marked[g], counts[g]);
            sum += distance;
            check = (check * 31 + distance + 1 + r) % 1000000007;
        }
    }
    printf("%d graphs of %lld nodes and %lld edges, %d rounds: distances sum to %lld, checksum %lld\n", graphs, (long long)n, (long long)m, rounds, (long long)sum, (long long)check);
    free(edges);
    return 0;
}
