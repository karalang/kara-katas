// Benchmark for #381: mirror of randomized_collection.kara (the ★ arm).
// C has no standard hash map, so the map from each value to its list of
// positions is a hand-written open-addressing table: power-of-two size,
// linear probing, one multiply for the hash, doubling when half full, and
// backward-shift deletion, so an emptied list's entry leaves no
// tombstone. A slot is empty when its `used` flag is 0.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t key;
    int64_t *list;
    int64_t len, cap;
    int used;
} Slot;

typedef struct {
    int64_t *vals, *slot;
    int64_t len, cap;
    Slot *table;
    int64_t nslots, keys;
    int64_t seed;
} RandomizedCollection;

static int64_t home(const RandomizedCollection *c, int64_t key) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ULL;
    return (int64_t)((h >> 32) & (uint64_t)(c->nslots - 1));
}

static int64_t find(const RandomizedCollection *c, int64_t key) {
    int64_t mask = c->nslots - 1, i = home(c, key);
    for (;;) {
        if (!c->table[i].used || c->table[i].key == key) return i;
        i = (i + 1) & mask;
    }
}

static void grow(RandomizedCollection *c) {
    Slot *old = c->table;
    int64_t n = c->nslots;
    c->nslots = 2 * n;
    c->table = calloc((size_t)c->nslots, sizeof(Slot));
    for (int64_t i = 0; i < n; i++)
        if (old[i].used) c->table[find(c, old[i].key)] = old[i];
    free(old);
}

static void push(int64_t **a, int64_t *len, int64_t *cap, int64_t x) {
    if (*len == *cap) {
        *cap = *cap ? 2 * *cap : 4;
        *a = realloc(*a, sizeof(int64_t) * (size_t)*cap);
    }
    (*a)[(*len)++] = x;
}

static void delete_slot(RandomizedCollection *c, int64_t i) {
    int64_t mask = c->nslots - 1, gap = i, j = (i + 1) & mask;
    free(c->table[gap].list);
    c->table[gap].used = 0;
    c->keys--;
    for (;;) {
        if (!c->table[j].used) return;
        int64_t h = home(c, c->table[j].key);
        int stays = gap <= j ? (gap < h && h <= j) : (gap < h || h <= j);
        if (!stays) {
            c->table[gap] = c->table[j];
            c->table[j].used = 0;
            gap = j;
        }
        j = (j + 1) & mask;
    }
}

static int insert(RandomizedCollection *c, int64_t val) {
    int64_t p = c->len;
    if (c->len == c->cap) {
        c->cap = c->cap ? 2 * c->cap : 8;
        c->vals = realloc(c->vals, sizeof(int64_t) * (size_t)c->cap);
        c->slot = realloc(c->slot, sizeof(int64_t) * (size_t)c->cap);
    }
    int64_t i = find(c, val);
    if (!c->table[i].used) {
        if (2 * (c->keys + 1) > c->nslots) {
            grow(c);
            i = find(c, val);
        }
        c->table[i] = (Slot){val, NULL, 0, 0, 1};
        c->keys++;
    }
    Slot *e = &c->table[i];
    c->vals[p] = val;
    c->slot[p] = e->len;
    c->len++;
    push(&e->list, &e->len, &e->cap, p);
    return e->len == 1;
}

static int remove_val(RandomizedCollection *c, int64_t val) {
    int64_t i = find(c, val);
    if (!c->table[i].used) return 0;
    int64_t p = c->table[i].list[--c->table[i].len];
    if (c->table[i].len == 0) delete_slot(c, i);
    int64_t last = c->len - 1;
    if (p < last) {
        int64_t moved = c->vals[last], k = c->slot[last];
        c->vals[p] = moved;
        c->slot[p] = k;
        c->table[find(c, moved)].list[k] = p;
    }
    c->len--;
    return 1;
}

static int64_t get_random(RandomizedCollection *c) {
    c->seed = (c->seed * 1103515245 + 12345) % 2147483648LL;
    return c->vals[(c->seed / 65536) % c->len];
}

int main(void) {
    RandomizedCollection c = {NULL, NULL, 0, 0, calloc(8, sizeof(Slot)), 8, 0, 381};
    int64_t seed = 381, checksum = 0;
    for (int64_t q = 0; q < 20000000; q++) {
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        int64_t op = (seed / 65536) % 3;
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        int64_t x = (seed / 64) % 100000;
        int64_t v;
        if (op == 0)
            v = insert(&c, x);
        else if (op == 1)
            v = remove_val(&c, x);
        else if (c.len > 0)
            v = get_random(&c) + 2;
        else
            v = 7;
        checksum = (checksum * 31 + v) % 1000000007;
    }
    printf("checksum %lld size %lld\n", (long long)checksum, (long long)c.len);
    for (int64_t i = 0; i < c.nslots; i++)
        if (c.table[i].used) free(c.table[i].list);
    free(c.table);
    free(c.vals);
    free(c.slot);
    return 0;
}
