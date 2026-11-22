// LeetCode #2714: Find Shortest Path with K Hops -- the bench (hops.kara in
// C): Dijkstra's search over states of a node and the hops spent, a
// binary heap of (distance, node, hops), smallest first. The tree edges
// and the pairs already joined are tracked in an n by n table, which
// holds the same set the other languages hash.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int64_t dist, node, hops; } Item;

typedef struct { Item *a; int64_t len, cap; } Heap;

static int less(Item x, Item y) {
    if (x.dist != y.dist) return x.dist < y.dist;
    if (x.node != y.node) return x.node < y.node;
    return x.hops < y.hops;
}

static void push(Heap *h, Item it) {
    if (h->len == h->cap) {
        h->cap = h->cap ? h->cap * 2 : 64;
        h->a = realloc(h->a, sizeof(Item) * (size_t)h->cap);
    }
    int64_t i = h->len++;
    h->a[i] = it;
    while (i > 0) {
        int64_t p = (i - 1) / 2;
        if (!less(h->a[i], h->a[p])) break;
        Item t = h->a[i]; h->a[i] = h->a[p]; h->a[p] = t;
        i = p;
    }
}

static Item pop(Heap *h) {
    Item top = h->a[0];
    h->a[0] = h->a[--h->len];
    int64_t i = 0;
    for (;;) {
        int64_t l = 2 * i + 1, r = l + 1, m = i;
        if (l < h->len && less(h->a[l], h->a[m])) m = l;
        if (r < h->len && less(h->a[r], h->a[m])) m = r;
        if (m == i) break;
        Item t = h->a[i]; h->a[i] = h->a[m]; h->a[m] = t;
        i = m;
    }
    return top;
}

typedef struct { int64_t to, w; } Arc;

static int64_t shortest_path_with_hops(int64_t n, const int64_t (*edges)[3], int64_t m, int64_t s, int64_t d, int64_t k) {
    int64_t *degree = calloc((size_t)n + 1, sizeof(int64_t));
    for (int64_t i = 0; i < m; i++) { degree[edges[i][0] + 1]++; degree[edges[i][1] + 1]++; }
    for (int64_t i = 0; i < n; i++) degree[i + 1] += degree[i];
    Arc *arcs = malloc(sizeof(Arc) * (size_t)(2 * m));
    int64_t *fill = malloc(sizeof(int64_t) * (size_t)n);
    memcpy(fill, degree, sizeof(int64_t) * (size_t)n);
    for (int64_t i = 0; i < m; i++) {
        arcs[fill[edges[i][0]]++] = (Arc){edges[i][1], edges[i][2]};
        arcs[fill[edges[i][1]]++] = (Arc){edges[i][0], edges[i][2]};
    }
    int64_t *dist = malloc(sizeof(int64_t) * (size_t)(n * (k + 1)));
    for (int64_t i = 0; i < n * (k + 1); i++) dist[i] = INT64_MAX;
    Heap h = {0};
    dist[s * (k + 1)] = 0;
    push(&h, (Item){0, s, 0});
    int64_t answer = -1;
    while (h.len > 0) {
        Item it = pop(&h);
        int64_t here = it.dist, u = it.node, hops = it.hops;
        if (here > dist[u * (k + 1) + hops]) continue;
        if (u == d) { answer = here; break; }
        for (int64_t a = degree[u]; a < degree[u + 1]; a++) {
            int64_t v = arcs[a].to, w = arcs[a].w;
            if (here + w < dist[v * (k + 1) + hops]) {
                dist[v * (k + 1) + hops] = here + w;
                push(&h, (Item){here + w, v, hops});
            }
            if (hops < k && here < dist[v * (k + 1) + hops + 1]) {
                dist[v * (k + 1) + hops + 1] = here;
                push(&h, (Item){here, v, hops + 1});
            }
        }
    }
    free(h.a); free(dist); free(fill); free(arcs); free(degree);
    return answer;
}

static int64_t seed = 2714;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

enum { GRAPHS = 50, ROUNDS = 10, N = 500, MOST = N - 1 + 9501 };

int main(void) {
    static int64_t edges[GRAPHS][MOST][3];
    static int64_t count[GRAPHS], src[GRAPHS], dst[GRAPHS], hop[GRAPHS];
    static unsigned char joined[N][N];
    for (int g = 0; g < GRAPHS; g++) {
        memset(joined, 0, sizeof joined);
        int64_t m = 0;
        for (int64_t v = 1; v < N; v++) {
            int64_t u = next_random() % v;
            joined[u][v] = 1;
            edges[g][m][0] = u; edges[g][m][1] = v; edges[g][m][2] = wide() % 1000000 + 1; m++;
        }
        for (int i = 0; i < 9501; i++) {
            int64_t a = next_random() % N, b = next_random() % N;
            int64_t u = a < b ? a : b, v = a < b ? b : a;
            if (u != v && !joined[u][v]) {
                joined[u][v] = 1;
                edges[g][m][0] = v; edges[g][m][1] = u; edges[g][m][2] = wide() % 1000000 + 1; m++;
            }
        }
        count[g] = m;
        src[g] = next_random() % N;
        dst[g] = (src[g] + 1 + next_random() % (N - 1)) % N;
        hop[g] = next_random() % 50;
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++) {
        for (int g = 0; g < GRAPHS; g++) {
            int64_t length = shortest_path_with_hops(N, (const int64_t (*)[3])edges[g], count[g], src[g], dst[g], hop[g]);
            sum += length;
            check = (check * 31 + length + r) % 1000000007;
        }
    }
    printf("%d graphs of 500 nodes, %d rounds: lengths sum to %lld, checksum %lld\n", GRAPHS, ROUNDS, (long long)sum, (long long)check);
    return 0;
}
