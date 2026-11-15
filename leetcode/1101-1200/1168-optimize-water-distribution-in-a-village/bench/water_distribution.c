// LeetCode #1168: Optimize Water Distribution in a Village -- the ★ arm's
// bench in C: Kruskal over the pipes and a pipe from a source to every
// house, union-find by size with path halving; the edges sorted by qsort on
// (cost, one end, the other).

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t c, a, b;
} Edge;

static int by_cost(const void *x, const void *y) {
    const Edge *p = x, *q = y;
    if (p->c != q->c) return p->c < q->c ? -1 : 1;
    if (p->a != q->a) return p->a < q->a ? -1 : 1;
    if (p->b != q->b) return p->b < q->b ? -1 : 1;
    return 0;
}

static int64_t find(int64_t *parent, int64_t x) {
    while (parent[x] != x) {
        parent[x] = parent[parent[x]];
        x = parent[x];
    }
    return x;
}

static int64_t min_cost(int64_t n, const int64_t *wells, const int64_t (*pipes)[3], int64_t m) {
    Edge *edges = malloc((n + m) * sizeof(Edge));
    int64_t e = 0;
    for (int64_t i = 0; i < n; i++) edges[e++] = (Edge){wells[i], 0, i + 1};
    for (int64_t j = 0; j < m; j++) edges[e++] = (Edge){pipes[j][2], pipes[j][0], pipes[j][1]};
    qsort(edges, e, sizeof(Edge), by_cost);
    int64_t *parent = malloc((n + 1) * sizeof(int64_t));
    int64_t *size = malloc((n + 1) * sizeof(int64_t));
    for (int64_t i = 0; i <= n; i++) {
        parent[i] = i;
        size[i] = 1;
    }
    int64_t cost = 0, joined = 0;
    for (int64_t k = 0; k < e; k++) {
        int64_t ra = find(parent, edges[k].a), rb = find(parent, edges[k].b);
        if (ra == rb) continue;
        if (size[ra] < size[rb]) {
            int64_t t = ra;
            ra = rb;
            rb = t;
        }
        parent[rb] = ra;
        size[ra] += size[rb];
        cost += edges[k].c;
        if (++joined == n) break;
    }
    free(edges);
    free(parent);
    free(size);
    return cost;
}

static int64_t seed = 1168;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

#define N 10000
#define M 10000

static int64_t wells[16][N];
static int64_t pipes[16][M][3];

int main(void) {
    for (int v = 0; v < 16; v++) {
        for (int i = 0; i < N; i++) wells[v][i] = next_random() % 100001;
        for (int j = 0; j < M; j++) {
            int64_t a = 1 + next_random() % N;
            int64_t b = 1 + next_random() % (N - 1);
            if (b >= a) b++;
            pipes[v][j][0] = a;
            pipes[v][j][1] = b;
            pipes[v][j][2] = next_random() % 100001;
        }
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < 40; r++) {
        for (int v = 0; v < 16; v++) {
            int64_t j = next_random() % M;
            pipes[v][j][2] = next_random() % 100001;
            int64_t c = min_cost(N, wells[v], (const int64_t(*)[3])pipes[v], M);
            total += c;
            check = (check * 31 + c) % 1000000007;
        }
    }
    printf("40 rounds over 16 villages of 10^4 houses: total %lld, checksum %lld\n", (long long)total,
           (long long)check);
    return 0;
}
