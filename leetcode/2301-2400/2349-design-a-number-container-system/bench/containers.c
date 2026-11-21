// LeetCode #2349: Design a Number Container System -- the bench, the ★ arm
// in C: a hash map from each index to its number, and a hash map from each
// number to a min-first binary heap of every index ever given it, popped
// lazily by find. Both maps are open addressing with linear probing over a
// mixed 64-bit key, grown at half full.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *keys, *vals;
    uint8_t *used;
    int64_t cap, len;
} Map;

static uint64_t mix(uint64_t x) {
    x ^= x >> 33;
    x *= 0xff51afd7ed558ccdULL;
    x ^= x >> 33;
    return x;
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

static int64_t *map_slot(Map *m, int64_t key, int insert);

static void map_grow(Map *m) {
    Map bigger;
    map_init(&bigger, m->cap * 2);
    for (int64_t i = 0; i < m->cap; i++)
        if (m->used[i]) *map_slot(&bigger, m->keys[i], 1) = m->vals[i];
    map_free(m);
    *m = bigger;
}

// The value slot of key, or NULL when it is absent and insert is 0.
static int64_t *map_slot(Map *m, int64_t key, int insert) {
    if (insert && 2 * (m->len + 1) > m->cap) map_grow(m);
    uint64_t i = mix((uint64_t)key) & (uint64_t)(m->cap - 1);
    while (m->used[i]) {
        if (m->keys[i] == key) return &m->vals[i];
        i = (i + 1) & (uint64_t)(m->cap - 1);
    }
    if (!insert) return NULL;
    m->used[i] = 1;
    m->keys[i] = key;
    m->len++;
    return &m->vals[i];
}

typedef struct {
    int64_t *xs;
    int64_t len, cap;
} Heap;

static void heap_push(Heap *h, int64_t x) {
    if (h->len == h->cap) {
        h->cap = h->cap ? 2 * h->cap : 4;
        h->xs = realloc(h->xs, h->cap * sizeof(int64_t));
    }
    int64_t i = h->len++;
    h->xs[i] = x;
    while (i > 0) {
        int64_t p = (i - 1) / 2;
        if (h->xs[p] <= h->xs[i]) break;
        int64_t t = h->xs[p];
        h->xs[p] = h->xs[i];
        h->xs[i] = t;
        i = p;
    }
}

static void heap_pop(Heap *h) {
    int64_t n = --h->len;
    h->xs[0] = h->xs[n];
    int64_t i = 0;
    for (;;) {
        int64_t l = 2 * i + 1, r = l + 1, m = i;
        if (l < n && h->xs[l] < h->xs[m]) m = l;
        if (r < n && h->xs[r] < h->xs[m]) m = r;
        if (m == i) break;
        int64_t t = h->xs[m];
        h->xs[m] = h->xs[i];
        h->xs[i] = t;
        i = m;
    }
}

typedef struct {
    Map at, heap_of;
    Heap *heaps;
    int64_t count, cap;
} NumberContainers;

static void nc_init(NumberContainers *c) {
    map_init(&c->at, 16);
    map_init(&c->heap_of, 16);
    c->heaps = NULL;
    c->count = c->cap = 0;
}

static void nc_free(NumberContainers *c) {
    for (int64_t i = 0; i < c->count; i++) free(c->heaps[i].xs);
    free(c->heaps);
    map_free(&c->at);
    map_free(&c->heap_of);
}

static void nc_change(NumberContainers *c, int64_t index, int64_t number) {
    *map_slot(&c->at, index, 1) = number;
    int64_t *id = map_slot(&c->heap_of, number, 0);
    if (!id) {
        if (c->count == c->cap) {
            c->cap = c->cap ? 2 * c->cap : 16;
            c->heaps = realloc(c->heaps, c->cap * sizeof(Heap));
        }
        c->heaps[c->count] = (Heap){NULL, 0, 0};
        id = map_slot(&c->heap_of, number, 1);
        *id = c->count++;
    }
    heap_push(&c->heaps[*id], index);
}

static int64_t nc_find(NumberContainers *c, int64_t number) {
    int64_t *id = map_slot(&c->heap_of, number, 0);
    if (!id) return -1;
    Heap *h = &c->heaps[*id];
    while (h->len > 0) {
        int64_t top = h->xs[0];
        if (*map_slot(&c->at, top, 0) == number) return top;
        heap_pop(h);
    }
    return -1;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245LL + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // two changes to every find, over 10^5 indices and 1000 numbers
    static int64_t kind[200000], a[200000], b[200000];
    int64_t seed = 2349;
    for (int i = 0; i < 200000; i++) {
        if (next_random(&seed) % 3 < 2) {
            int64_t high = next_random(&seed);
            kind[i] = 0;
            a[i] = (high * 32768 + next_random(&seed)) % 100000 + 1;
            b[i] = next_random(&seed) % 1000 + 1;
        } else {
            kind[i] = 1;
            a[i] = next_random(&seed) % 1000 + 1;
            b[i] = 0;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 20; p++) {
        NumberContainers c;
        nc_init(&c);
        for (int i = 0; i < 200000; i++) {
            if (kind[i] == 0)
                nc_change(&c, a[i], b[i]);
            else
                check = (check * 31 + nc_find(&c, a[i]) + p + 2) % 1000000007;
        }
        nc_free(&c);
    }
    printf("20 passes over 2 * 10^5 calls: checksum %lld\n", (long long)check);
    return 0;
}
