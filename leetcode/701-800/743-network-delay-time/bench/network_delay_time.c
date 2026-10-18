// LeetCode 743 — Network Delay Time, bench: the ★ arm (Dijkstra with a
// priority queue) on a 100-node graph of 6000 edges, every source, while
// edge times change. Mirrors network_delay_time.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t v, w; } Edge;
typedef struct { Edge *items; int64_t len, cap; } EdgeVec;
typedef struct { int64_t d, u; } Entry;
typedef struct { Entry *items; int64_t len, cap; } Heap;
typedef struct { int64_t u, v, w; } Time;

static int less(Entry a, Entry b) { return a.d < b.d || (a.d == b.d && a.u < b.u); }

static void heap_push(Heap *h, Entry e) {
    if (h->len == h->cap) {
        h->cap = h->cap ? 2 * h->cap : 4;
        h->items = realloc(h->items, h->cap * sizeof(Entry));
    }
    int64_t i = h->len++;
    while (i > 0) {
        int64_t p = (i - 1) / 2;
        if (!less(e, h->items[p])) break;
        h->items[i] = h->items[p];
        i = p;
    }
    h->items[i] = e;
}

static Entry heap_pop(Heap *h) {
    Entry top = h->items[0];
    Entry last = h->items[--h->len];
    int64_t i = 0;
    for (;;) {
        int64_t c = 2 * i + 1;
        if (c >= h->len) break;
        if (c + 1 < h->len && less(h->items[c + 1], h->items[c])) c++;
        if (!less(h->items[c], last)) break;
        h->items[i] = h->items[c];
        i = c;
    }
    if (h->len > 0) h->items[i] = last;
    return top;
}

static int64_t network_delay_time(const Time *times, int64_t m, int64_t n, int64_t k) {
    EdgeVec *adj = calloc(n + 1, sizeof(EdgeVec));
    for (int64_t i = 0; i < m; i++) {
        EdgeVec *a = &adj[times[i].u];
        if (a->len == a->cap) {
            a->cap = a->cap ? 2 * a->cap : 4;
            a->items = realloc(a->items, a->cap * sizeof(Edge));
        }
        a->items[a->len++] = (Edge){times[i].v, times[i].w};
    }
    int64_t *heard = malloc((n + 1) * sizeof(int64_t));
    for (int64_t i = 0; i <= n; i++) heard[i] = -1;
    Heap queue = {0};
    heap_push(&queue, (Entry){0, k});
    int64_t settled = 0, last = 0;
    while (queue.len > 0) {
        Entry e = heap_pop(&queue);
        int64_t d = e.d, u = e.u;
        if (heard[u] != -1) continue;
        heard[u] = d;
        settled++;
        last = d;
        for (int64_t j = 0; j < adj[u].len; j++) {
            int64_t v = adj[u].items[j].v, w = adj[u].items[j].w;
            if (heard[v] == -1) heap_push(&queue, (Entry){d + w, v});
        }
    }
    for (int64_t i = 0; i <= n; i++) free(adj[i].items);
    free(adj);
    free(heard);
    free(queue.items);
    return settled == n ? last : -1;
}

static int64_t seed = 743;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t rounds = 12, n = 100, m = 6000, max_w = 100;
    char *used = calloc((n + 1) * (n + 1), 1);
    Time *times = malloc(m * sizeof(Time));
    int64_t len = 0;
    while (len < m) {
        int64_t u = 1 + next_random() % n;
        int64_t v = 1 + next_random() % n;
        if (u == v || used[u * (n + 1) + v]) continue;
        used[u * (n + 1) + v] = 1;
        int64_t w = next_random() % (max_w + 1);
        times[len++] = (Time){u, v, w};
    }
    int64_t total = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < 50; c++) {
            int64_t i = next_random() % m;
            int64_t w = next_random() % 101;
            times[i].w = w;
        }
        for (int64_t k = 1; k <= n; k++) total += network_delay_time(times, m, n, k);
    }
    printf("%lld rounds of 100 queries on 100 nodes and 6000 edges: answers sum to %lld\n",
           (long long)rounds, (long long)total);
    free(used);
    free(times);
    return 0;
}
