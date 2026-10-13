// Benchmark for #460: mirror of lfu_cache.kara (the ★ arm, a linked list
// per use count) on the same workload. C has no hash map, so this file
// carries a small open-addressing one (linear probing, backward-shift
// deletion) for the key and count lookups.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *keys;
    int64_t *values;
    bool *used;
    int64_t mask;
    int64_t len;
} Table;

static Table table_new(int64_t slots) {
    Table t = {calloc(slots, sizeof(int64_t)), calloc(slots, sizeof(int64_t)), calloc(slots, sizeof(bool)), slots - 1, 0};
    return t;
}

static int64_t slot_of(const Table *t, int64_t key) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ULL;
    return (int64_t)(h >> 20) & t->mask;
}

static bool table_get(const Table *t, int64_t key, int64_t *value) {
    for (int64_t i = slot_of(t, key);; i = (i + 1) & t->mask) {
        if (!t->used[i]) {
            return false;
        }
        if (t->keys[i] == key) {
            *value = t->values[i];
            return true;
        }
    }
}

static void table_insert(Table *t, int64_t key, int64_t value) {
    int64_t i = slot_of(t, key);
    while (t->used[i] && t->keys[i] != key) {
        i = (i + 1) & t->mask;
    }
    if (!t->used[i]) {
        t->len++;
    }
    t->used[i] = true;
    t->keys[i] = key;
    t->values[i] = value;
}

static void table_remove(Table *t, int64_t key) {
    int64_t i = slot_of(t, key);
    while (t->used[i] && t->keys[i] != key) {
        i = (i + 1) & t->mask;
    }
    if (!t->used[i]) {
        return;
    }
    t->used[i] = false;
    t->len--;
    for (int64_t j = (i + 1) & t->mask; t->used[j]; j = (j + 1) & t->mask) {
        int64_t home = slot_of(t, t->keys[j]);
        // Move j back to i unless its home lies cyclically in (i, j].
        bool stays = (i <= j) ? (i < home && home <= j) : (i < home || home <= j);
        if (!stays) {
            t->used[i] = true;
            t->keys[i] = t->keys[j];
            t->values[i] = t->values[j];
            t->used[j] = false;
            i = j;
        }
    }
}

typedef struct {
    int64_t key, value, count, prev, next;
} Node;

typedef struct {
    int64_t capacity;
    Node *nodes;
    int64_t len, cap;
    Table index;
    Table sentinels;
    int64_t least;
    int64_t free;
} LFUCache;

static int64_t push_node(LFUCache *c, Node n) {
    if (c->len == c->cap) {
        c->cap = c->cap ? c->cap * 2 : 16;
        c->nodes = realloc(c->nodes, c->cap * sizeof(Node));
    }
    c->nodes[c->len] = n;
    return c->len++;
}

static void unlink_node(LFUCache *c, int64_t i) {
    int64_t prev = c->nodes[i].prev, next = c->nodes[i].next;
    c->nodes[prev].next = next;
    c->nodes[next].prev = prev;
}

static void append_node(LFUCache *c, int64_t i, int64_t count) {
    int64_t s;
    if (!table_get(&c->sentinels, count, &s)) {
        s = c->len;
        push_node(c, (Node){-1, 0, count, s, s});
        table_insert(&c->sentinels, count, s);
    }
    int64_t last = c->nodes[s].prev;
    c->nodes[i].count = count;
    c->nodes[i].prev = last;
    c->nodes[i].next = s;
    c->nodes[last].next = i;
    c->nodes[s].prev = i;
}

static bool is_empty(LFUCache *c, int64_t count) {
    int64_t s;
    table_get(&c->sentinels, count, &s);
    return c->nodes[s].next == s;
}

static void touch(LFUCache *c, int64_t i) {
    int64_t count = c->nodes[i].count;
    unlink_node(c, i);
    if (c->least == count && is_empty(c, count)) {
        c->least = count + 1;
    }
    append_node(c, i, count + 1);
}

static int64_t cache_get(LFUCache *c, int64_t key) {
    int64_t i;
    if (!table_get(&c->index, key, &i)) {
        return -1;
    }
    touch(c, i);
    return c->nodes[i].value;
}

static void cache_put(LFUCache *c, int64_t key, int64_t value) {
    if (c->capacity == 0) {
        return;
    }
    int64_t i;
    if (table_get(&c->index, key, &i)) {
        c->nodes[i].value = value;
        touch(c, i);
        return;
    }
    if (c->index.len == c->capacity) {
        int64_t s;
        table_get(&c->sentinels, c->least, &s);
        int64_t victim = c->nodes[s].next;
        unlink_node(c, victim);
        table_remove(&c->index, c->nodes[victim].key);
        c->free = victim;
    }
    if (c->free >= 0) {
        i = c->free;
        c->free = -1;
        c->nodes[i].key = key;
        c->nodes[i].value = value;
    } else {
        i = push_node(c, (Node){key, value, 0, -1, -1});
    }
    table_insert(&c->index, key, i);
    append_node(c, i, 1);
    c->least = 1;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t capacity = 4096;
    const int64_t calls = 10000000;
    int64_t seed = 460;
    // The tables are sized for this workload: 4,096 keys, and fewer than
    // 2^19 distinct use counts.
    LFUCache cache = {capacity, NULL, 0, 0, table_new(1 << 14), table_new(1 << 20), 0, -1};
    int64_t hits = 0;
    int64_t checksum = 0;
    for (int64_t n = 0; n < calls; n++) {
        int64_t a = next_random(&seed) % 200;
        int64_t b = next_random(&seed) % 200;
        int64_t key = a * b;
        if (next_random(&seed) % 2 == 0) {
            int64_t value = next_random(&seed) % 1000000;
            cache_put(&cache, key, value);
        } else {
            int64_t answer = cache_get(&cache, key);
            if (answer >= 0) {
                hits += 1;
            }
            checksum = (checksum * 31 + answer + 2) % 1000000007;
        }
    }
    printf("%lld calls on a cache of %lld: %lld hits, checksum %lld\n", (long long)calls,
           (long long)capacity, (long long)hits, (long long)checksum);
    return 0;
}
