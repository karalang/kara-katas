// LeetCode #2034: Stock Price Fluctuation -- the ★ arm in C, the same
// algorithm and workload as stock.kara: a hash map of prices (open
// addressing, linear probing, a multiplicative hash), the latest
// timestamp, and two binary heaps of (price, timestamp) records with stale
// ones popped at query time.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int64_t price, ts; } Rec;

typedef struct {
    int64_t *keys, *vals;
    uint8_t *used;
    int64_t cap, len;
} Map;

static uint64_t hash64(int64_t k) {
    uint64_t x = (uint64_t)k * 0x9E3779B97F4A7C15ULL;
    return x ^ (x >> 29);
}

static void map_init(Map *m, int64_t cap) {
    m->cap = cap;
    m->len = 0;
    m->keys = malloc(cap * sizeof(int64_t));
    m->vals = malloc(cap * sizeof(int64_t));
    m->used = calloc(cap, 1);
}

static void map_free(Map *m) {
    free(m->keys);
    free(m->vals);
    free(m->used);
}

static void map_put(Map *m, int64_t k, int64_t v);

static void map_grow(Map *m) {
    Map n;
    map_init(&n, m->cap * 2);
    for (int64_t i = 0; i < m->cap; i++)
        if (m->used[i]) map_put(&n, m->keys[i], m->vals[i]);
    map_free(m);
    *m = n;
}

static void map_put(Map *m, int64_t k, int64_t v) {
    if ((m->len + 1) * 4 > m->cap * 3) map_grow(m);
    uint64_t i = hash64(k) & (uint64_t)(m->cap - 1);
    while (m->used[i] && m->keys[i] != k) i = (i + 1) & (uint64_t)(m->cap - 1);
    if (!m->used[i]) {
        m->used[i] = 1;
        m->keys[i] = k;
        m->len++;
    }
    m->vals[i] = v;
}

static int64_t map_get(const Map *m, int64_t k) {
    uint64_t i = hash64(k) & (uint64_t)(m->cap - 1);
    while (m->keys[i] != k || !m->used[i]) i = (i + 1) & (uint64_t)(m->cap - 1);
    return m->vals[i];
}

typedef struct {
    Rec *a;
    int64_t len, cap;
    int max_first;
} Heap;

static int before(const Heap *h, Rec x, Rec y) {
    int less = x.price < y.price || (x.price == y.price && x.ts < y.ts);
    int more = x.price > y.price || (x.price == y.price && x.ts > y.ts);
    return h->max_first ? more : less;
}

static void heap_push(Heap *h, Rec r) {
    if (h->len == h->cap) {
        h->cap = h->cap ? h->cap * 2 : 16;
        h->a = realloc(h->a, h->cap * sizeof(Rec));
    }
    int64_t i = h->len++;
    while (i > 0) {
        int64_t p = (i - 1) / 2;
        if (!before(h, r, h->a[p])) break;
        h->a[i] = h->a[p];
        i = p;
    }
    h->a[i] = r;
}

static void heap_pop(Heap *h) {
    Rec last = h->a[--h->len];
    int64_t i = 0;
    for (;;) {
        int64_t c = 2 * i + 1;
        if (c >= h->len) break;
        if (c + 1 < h->len && before(h, h->a[c + 1], h->a[c])) c++;
        if (!before(h, h->a[c], last)) break;
        h->a[i] = h->a[c];
        i = c;
    }
    if (h->len > 0) h->a[i] = last;
}

typedef struct {
    Map prices;
    int64_t latest;
    Heap highs, lows;
} StockPrice;

static void stock_init(StockPrice *s) {
    map_init(&s->prices, 16);
    s->latest = 0;
    s->highs = (Heap){NULL, 0, 0, 1};
    s->lows = (Heap){NULL, 0, 0, 0};
}

static void stock_free(StockPrice *s) {
    map_free(&s->prices);
    free(s->highs.a);
    free(s->lows.a);
}

static void update(StockPrice *s, int64_t ts, int64_t price) {
    map_put(&s->prices, ts, price);
    if (ts > s->latest) s->latest = ts;
    heap_push(&s->highs, (Rec){price, ts});
    heap_push(&s->lows, (Rec){price, ts});
}

static int64_t current(StockPrice *s) { return map_get(&s->prices, s->latest); }

static int64_t extreme(StockPrice *s, Heap *h) {
    for (;;) {
        Rec r = h->a[0];
        if (map_get(&s->prices, r.ts) == r.price) return r.price;
        heap_pop(h);
    }
}

static int64_t seed = 2034;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct { int64_t kind, ts, price; } Op;

int main(void) {
    static Op sessions[10][100000];
    const int64_t spans[5] = {1000000000, 100000, 1000, 1000000000, 50000};
    const int64_t tops[5] = {1000000000, 1000, 1000000000, 100, 1000000};
    for (int a = 0; a < 10; a++) {
        int64_t span = spans[a % 5], top = tops[a % 5], upd = a % 7 + 2;
        for (int i = 0; i < 100000; i++) {
            if (i == 0 || next_random() % 10 < upd) {
                int64_t hi = next_random(), lo = next_random();
                int64_t ts = (hi * 32768 + lo) % span + 1;
                hi = next_random();
                lo = next_random();
                int64_t price = (hi * 32768 + lo) % top + 1;
                sessions[a][i] = (Op){0, ts, price};
            } else {
                sessions[a][i] = (Op){next_random() % 3 + 1, 0, 0};
            }
        }
    }
    int64_t runs = 0, queries = 0, check = 0;
    for (int round = 0; round < 15; round++) {
        for (int a = 0; a < 10; a++) {
            StockPrice s;
            stock_init(&s);
            for (int i = 0; i < 100000; i++) {
                Op op = sessions[a][i];
                if (op.kind == 0) {
                    update(&s, op.ts, op.price);
                } else {
                    int64_t answer = op.kind == 1 ? current(&s) : op.kind == 2 ? extreme(&s, &s.highs) : extreme(&s, &s.lows);
                    queries++;
                    check = (check * 31 + answer % 1000000007 + op.kind) % 1000000007;
                }
            }
            stock_free(&s);
            runs++;
        }
    }
    printf("%lld sessions: %lld queries, checksum %lld\n", (long long)runs, (long long)queries, (long long)check);
    return 0;
}
