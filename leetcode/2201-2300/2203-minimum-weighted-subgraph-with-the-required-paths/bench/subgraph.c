// benchmark's C mirror of subgraph.kara (LeetCode #2203, the ★ arm): three
// Dijkstras with a binary heap of (distance, node) pairs, the last over
// the edges turned round, and the least sum over the meeting node. Each
// node's out-edges are a growable array, as Kāra's `Vec[Vec[..]]`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t to, w;
} arc_t;

typedef struct {
    arc_t *a;
    int64_t len, cap;
} list_t;

static void list_push(list_t *l, int64_t to, int64_t w) {
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->a = realloc(l->a, sizeof(arc_t) * (size_t)l->cap);
    }
    l->a[l->len].to = to;
    l->a[l->len].w = w;
    l->len++;
}

typedef struct {
    int64_t d, u;
} item_t;

typedef struct {
    item_t *h;
    int64_t len, cap;
} heap_t;

static int less(item_t x, item_t y) { return x.d < y.d || (x.d == y.d && x.u < y.u); }

static void heap_push(heap_t *q, int64_t d, int64_t u) {
    if (q->len == q->cap) {
        q->cap = q->cap ? q->cap * 2 : 16;
        q->h = realloc(q->h, sizeof(item_t) * (size_t)q->cap);
    }
    int64_t i = q->len++;
    item_t it = {d, u};
    while (i > 0) {
        int64_t p = (i - 1) / 2;
        if (!less(it, q->h[p])) break;
        q->h[i] = q->h[p];
        i = p;
    }
    q->h[i] = it;
}

static item_t heap_pop(heap_t *q) {
    item_t top = q->h[0];
    item_t last = q->h[--q->len];
    int64_t i = 0;
    for (;;) {
        int64_t c = 2 * i + 1;
        if (c >= q->len) break;
        if (c + 1 < q->len && less(q->h[c + 1], q->h[c])) c++;
        if (!less(q->h[c], last)) break;
        q->h[i] = q->h[c];
        i = c;
    }
    if (q->len > 0) q->h[i] = last;
    return top;
}

static int64_t *dijkstra(const list_t *adj, int64_t n, int64_t from) {
    int64_t *dist = malloc(sizeof(int64_t) * (size_t)n);
    for (int64_t i = 0; i < n; i++) dist[i] = -1;
    heap_t q = {0};
    heap_push(&q, 0, from);
    while (q.len > 0) {
        item_t it = heap_pop(&q);
        if (dist[it.u] >= 0) continue;
        dist[it.u] = it.d;
        const list_t *l = &adj[it.u];
        for (int64_t j = 0; j < l->len; j++)
            if (dist[l->a[j].to] < 0) heap_push(&q, it.d + l->a[j].w, l->a[j].to);
    }
    free(q.h);
    return dist;
}

static int64_t minimum_weight(int64_t n, const int64_t (*edges)[3], int64_t m, int64_t src1, int64_t src2, int64_t dest) {
    list_t *forward = calloc((size_t)n, sizeof(list_t));
    list_t *backward = calloc((size_t)n, sizeof(list_t));
    for (int64_t i = 0; i < m; i++) {
        list_push(&forward[edges[i][0]], edges[i][1], edges[i][2]);
        list_push(&backward[edges[i][1]], edges[i][0], edges[i][2]);
    }
    int64_t *one = dijkstra(forward, n, src1);
    int64_t *two = dijkstra(forward, n, src2);
    int64_t *home = dijkstra(backward, n, dest);
    int64_t best = -1;
    for (int64_t v = 0; v < n; v++)
        if (one[v] >= 0 && two[v] >= 0 && home[v] >= 0) {
            int64_t total = one[v] + two[v] + home[v];
            if (best < 0 || total < best) best = total;
        }
    for (int64_t v = 0; v < n; v++) {
        free(forward[v].a);
        free(backward[v].a);
    }
    free(forward);
    free(backward);
    free(one);
    free(two);
    free(home);
    return best;
}

static int64_t seed = 2203;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t hi = next_random();
    return hi * 32768 + next_random();
}

int main(void) {
    const int64_t n = 20000, m = 60000;
    static int64_t graphs[4][60000][3];
    for (int g = 0; g < 4; g++) {
        int64_t len = 0;
        while (len < m) {
            int64_t from = wide_random() % n;
            int64_t to = wide_random() % n;
            if (from != to) {
                graphs[g][len][0] = from;
                graphs[g][len][1] = to;
                graphs[g][len][2] = wide_random() % 100000 + 1;
                len++;
            }
        }
    }
    int64_t check = 0;
    for (int pass = 0; pass < 5; pass++)
        for (int g = 0; g < 4; g++)
            for (int64_t t = 0; t < 4; t++) {
                int64_t weight = minimum_weight(n, (const int64_t (*)[3])graphs[g], m, t * 3, t * 3 + 1, t * 3 + 2);
                check = (check * 31 + weight + 1) % 1000000007;
            }
    printf("5 passes over 4 graphs: checksum %lld\n", (long long)check);
    return 0;
}
