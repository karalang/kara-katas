// Benchmark for #380: mirror of randomized_set.kara (the open-addressing
// arm). A slot is empty when its `used` flag is 0.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t val, pos;
    int used;
} Slot;

typedef struct {
    int64_t *vals;
    int64_t len, cap;
    Slot *slots;
    int64_t nslots;
    int64_t seed;
} RandomizedSet;

static int64_t home(const RandomizedSet *s, int64_t val) {
    uint64_t h = (uint64_t)val * 0x9E3779B97F4A7C15ULL;
    return (int64_t)((h >> 32) & (uint64_t)(s->nslots - 1));
}

static int64_t find(const RandomizedSet *s, int64_t val) {
    int64_t mask = s->nslots - 1, i = home(s, val);
    for (;;) {
        if (!s->slots[i].used || s->slots[i].val == val) return i;
        i = (i + 1) & mask;
    }
}

static void set_position(RandomizedSet *s, int64_t val, int64_t pos) {
    int64_t i = find(s, val);
    s->slots[i] = (Slot){val, pos, 1};
}

static void grow(RandomizedSet *s) {
    Slot *old = s->slots;
    int64_t n = s->nslots;
    s->nslots = 2 * n;
    s->slots = calloc((size_t)s->nslots, sizeof(Slot));
    for (int64_t i = 0; i < n; i++)
        if (old[i].used) set_position(s, old[i].val, old[i].pos);
    free(old);
}

static int insert(RandomizedSet *s, int64_t val) {
    if (s->slots[find(s, val)].used) return 0;
    if (2 * (s->len + 1) > s->nslots) grow(s);
    set_position(s, val, s->len);
    if (s->len == s->cap) {
        s->cap = s->cap ? 2 * s->cap : 8;
        s->vals = realloc(s->vals, sizeof(int64_t) * (size_t)s->cap);
    }
    s->vals[s->len++] = val;
    return 1;
}

static void delete_slot(RandomizedSet *s, int64_t i) {
    int64_t mask = s->nslots - 1, gap = i, j = (i + 1) & mask;
    s->slots[gap].used = 0;
    for (;;) {
        if (!s->slots[j].used) return;
        int64_t h = home(s, s->slots[j].val);
        int stays = gap <= j ? (gap < h && h <= j) : (gap < h || h <= j);
        if (!stays) {
            s->slots[gap] = s->slots[j];
            s->slots[j].used = 0;
            gap = j;
        }
        j = (j + 1) & mask;
    }
}

static int remove_val(RandomizedSet *s, int64_t val) {
    int64_t i = find(s, val);
    if (!s->slots[i].used) return 0;
    int64_t pos = s->slots[i].pos;
    delete_slot(s, i);
    int64_t last = s->vals[--s->len];
    if (pos < s->len) {
        s->vals[pos] = last;
        set_position(s, last, pos);
    }
    return 1;
}

static int64_t get_random(RandomizedSet *s) {
    s->seed = (s->seed * 1103515245 + 12345) % 2147483648LL;
    return s->vals[(s->seed / 65536) % s->len];
}

int main(void) {
    RandomizedSet s = {NULL, 0, 0, calloc(8, sizeof(Slot)), 8, 380};
    int64_t seed = 380, checksum = 0;
    for (int64_t q = 0; q < 20000000; q++) {
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        int64_t op = (seed / 65536) % 3;
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        int64_t x = (seed / 64) % 200000;
        int64_t v;
        if (op == 0)
            v = insert(&s, x);
        else if (op == 1)
            v = remove_val(&s, x);
        else if (s.len > 0)
            v = get_random(&s);
        else
            v = 7;
        checksum = (checksum * 31 + v) % 1000000007;
    }
    printf("checksum %lld size %lld\n", (long long)checksum, (long long)s.len);
    free(s.vals);
    free(s.slots);
    return 0;
}
