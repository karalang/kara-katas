// LeetCode #2097: Valid Arrangement of Pairs -- C mirror of the ★ arm's
// benchmark (arrangement.kara): the same 100 random walks of 100000 pairs,
// each arranged by Hierholzer's walk on an explicit stack. C has no map, so
// each value is given a number by an open-addressing table, and each
// number keeps a growable array of the values its pairs lead to and an
// out-minus-in balance; a second table holds the pairs the walks have
// used.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t a, b;
} Pair;

typedef struct {
    int64_t *items;
    int64_t len, cap;
} Vec;

static void vec_push(Vec *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->items = realloc(v->items, (size_t)v->cap * sizeof(int64_t));
    }
    v->items[v->len++] = x;
}

typedef struct {
    int64_t *keys;
    int64_t *ids;
    int64_t cap, count;
    Vec *next;
    int64_t *balance;
    int64_t *value;
} Table;

static uint64_t mix(int64_t k) {
    uint64_t x = (uint64_t)k;
    x ^= x >> 33;
    x *= 0xff51afd7ed558ccdULL;
    x ^= x >> 33;
    return x;
}

static int64_t id_of(Table *t, int64_t key) {
    uint64_t h = mix(key) & (uint64_t)(t->cap - 1);
    while (t->ids[h] >= 0) {
        if (t->keys[h] == key) return t->ids[h];
        h = (h + 1) & (uint64_t)(t->cap - 1);
    }
    int64_t id = t->count++;
    t->keys[h] = key;
    t->ids[h] = id;
    t->value[id] = key;
    t->next[id] = (Vec){0};
    t->balance[id] = 0;
    return id;
}

// the arrangement into `out`, which has room for `n` pairs
static void valid_arrangement(const Pair *pairs, int64_t n, Pair *out) {
    Table t;
    t.cap = 1;
    while (t.cap < 4 * (2 * n + 1)) t.cap *= 2;
    t.keys = malloc((size_t)t.cap * sizeof(int64_t));
    t.ids = malloc((size_t)t.cap * sizeof(int64_t));
    memset(t.ids, 0xff, (size_t)t.cap * sizeof(int64_t));
    t.count = 0;
    t.next = malloc((size_t)(2 * n + 1) * sizeof(Vec));
    t.balance = malloc((size_t)(2 * n + 1) * sizeof(int64_t));
    t.value = malloc((size_t)(2 * n + 1) * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        int64_t a = id_of(&t, pairs[i].a);
        int64_t b = id_of(&t, pairs[i].b);
        vec_push(&t.next[a], b);
        t.balance[a] += 1;
        t.balance[b] -= 1;
    }
    int64_t start = id_of(&t, pairs[0].a);
    for (int64_t v = 0; v < t.count; v++) {
        if (t.balance[v] == 1) start = v;
    }
    int64_t *stack = malloc((size_t)(n + 2) * sizeof(int64_t));
    int64_t *path = malloc((size_t)(n + 2) * sizeof(int64_t));
    int64_t top_at = 0, plen = 0;
    stack[top_at++] = start;
    while (top_at > 0) {
        int64_t top = stack[top_at - 1];
        Vec *outs = &t.next[top];
        if (outs->len > 0) {
            stack[top_at++] = outs->items[--outs->len];
        } else {
            path[plen++] = top;
            top_at--;
        }
    }
    for (int64_t i = 1; i < plen; i++) {
        out[i - 1].a = t.value[path[plen - i]];
        out[i - 1].b = t.value[path[plen - i - 1]];
    }
    for (int64_t v = 0; v < t.count; v++) free(t.next[v].items);
    free(t.keys);
    free(t.ids);
    free(t.next);
    free(t.balance);
    free(t.value);
    free(stack);
    free(path);
}

static int64_t seed = 2097;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t hi = next_random();
    return hi * 32768 + next_random();
}

// a set of pairs: open addressing over the key a * (10^9 + 1) + b, which
// is below 2^63 for values up to 10^9
typedef struct {
    int64_t *keys;
    int64_t cap;
} PairSet;

static int64_t *pair_slot(PairSet *s, int64_t a, int64_t b) {
    int64_t key = a * 1000000001 + b;
    uint64_t h = mix(key) & (uint64_t)(s->cap - 1);
    while (s->keys[h] >= 0 && s->keys[h] != key) h = (h + 1) & (uint64_t)(s->cap - 1);
    return &s->keys[h];
}

static int pair_used(PairSet *s, int64_t a, int64_t b) {
    return *pair_slot(s, a, b) >= 0;
}

static void pair_add(PairSet *s, int64_t a, int64_t b) {
    *pair_slot(s, a, b) = a * 1000000001 + b;
}

// a step from `at` to a value it has no pair to yet, or -1
static int64_t step(int64_t at, const int64_t *values, int64_t k, PairSet *used) {
    int64_t from = next_random() % k;
    for (int64_t j = 0; j < k; j++) {
        int64_t v = values[(from + j) % k];
        if (v != at && !pair_used(used, at, v)) return v;
    }
    return -1;
}

// the walk's pairs into `pairs` (room for m + 50), their count returned
static int64_t random_pairs(int64_t m, int64_t k, int closed, Pair *pairs) {
    int64_t *values = malloc((size_t)k * sizeof(int64_t));
    for (int64_t i = 0; i < k; i++) values[i] = wide_random() % 1000000001;
    int64_t *walk = malloc((size_t)(m + 52) * sizeof(int64_t));
    PairSet used;
    used.cap = 1;
    while (used.cap < 4 * (m + 52)) used.cap *= 2;
    used.keys = malloc((size_t)used.cap * sizeof(int64_t));
    memset(used.keys, 0xff, (size_t)used.cap * sizeof(int64_t));
    int64_t first = values[next_random() % k];
    int64_t len = 0;
    walk[len++] = first;
    int64_t at = first;
    while (len <= m + 50) {
        if (closed && len >= m && at != first && !pair_used(&used, at, first)) {
            walk[len++] = first;
            break;
        }
        if (!closed && len > m) break;
        int64_t v = step(at, values, k, &used);
        if (v < 0) break;
        pair_add(&used, at, v);
        walk[len++] = v;
        at = v;
    }
    int64_t n = len - 1;
    for (int64_t i = 1; i < len; i++) {
        pairs[i - 1].a = walk[i - 1];
        pairs[i - 1].b = walk[i];
    }
    for (int64_t i = n - 1; i > 0; i--) {
        int64_t j = wide_random() % (i + 1);
        Pair tmp = pairs[i];
        pairs[i] = pairs[j];
        pairs[j] = tmp;
    }
    free(values);
    free(walk);
    free(used.keys);
    return n;
}

int main(void) {
    const int64_t m = 100000;
    Pair *pairs = malloc((size_t)(m + 52) * sizeof(Pair));
    Pair *got = malloc((size_t)(m + 52) * sizeof(Pair));
    int64_t total = 0, check = 0;
    for (int round = 0; round < 100; round++) {
        int64_t n = random_pairs(m, 1000, round % 2 == 0, pairs);
        valid_arrangement(pairs, n, got);
        total += n;
        for (int64_t i = 0; i < n; i++) check = (check * 31 + got[i].a) % 1000000007;
        check = (check * 31 + got[n - 1].b) % 1000000007;
    }
    printf("100 rounds: %lld pairs, checksum %lld\n", (long long)total, (long long)check);
    free(pairs);
    free(got);
    return 0;
}
