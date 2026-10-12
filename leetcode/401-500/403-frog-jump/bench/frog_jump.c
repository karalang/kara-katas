// Benchmark for #403: mirror of frog_jump.kara (the jump sizes that reach
// each stone). C has no map or set type, so the map from a stone's
// position to its jump sizes is an open-addressing table of positions,
// and each stone's jump sizes are a growable open-addressing set, as the
// other mirrors' hash maps and sets are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *keys;  // -1 marks an empty slot
    int64_t len, cap;
} IntSet;

static uint64_t mix(int64_t x) {
    uint64_t h = (uint64_t)x * 0x9E3779B97F4A7C15ULL;
    return h ^ (h >> 29);
}

static void set_init(IntSet *s, int64_t cap) {
    s->cap = cap;
    s->len = 0;
    s->keys = malloc(cap * sizeof(int64_t));
    for (int64_t i = 0; i < cap; i++) s->keys[i] = -1;
}

static int set_insert(IntSet *s, int64_t key);

static void set_grow(IntSet *s) {
    IntSet bigger;
    set_init(&bigger, s->cap * 2);
    for (int64_t i = 0; i < s->cap; i++) {
        if (s->keys[i] >= 0) set_insert(&bigger, s->keys[i]);
    }
    free(s->keys);
    *s = bigger;
}

static int set_insert(IntSet *s, int64_t key) {
    if ((s->len + 1) * 4 > s->cap * 3) set_grow(s);
    uint64_t at = mix(key) & (s->cap - 1);
    while (s->keys[at] >= 0) {
        if (s->keys[at] == key) return 0;
        at = (at + 1) & (s->cap - 1);
    }
    s->keys[at] = key;
    s->len++;
    return 1;
}

typedef struct {
    int64_t *pos;  // -1 marks an empty slot
    IntSet *sets;
    int64_t cap;
} Map;

static IntSet *map_get(Map *m, int64_t key) {
    uint64_t at = mix(key) & (m->cap - 1);
    while (m->pos[at] >= 0) {
        if (m->pos[at] == key) return &m->sets[at];
        at = (at + 1) & (m->cap - 1);
    }
    return NULL;
}

static int can_cross(const int64_t *stones, int64_t n) {
    Map jumps;
    jumps.cap = 1;
    while (jumps.cap < n * 2) jumps.cap *= 2;
    jumps.pos = malloc(jumps.cap * sizeof(int64_t));
    jumps.sets = malloc(jumps.cap * sizeof(IntSet));
    for (int64_t i = 0; i < jumps.cap; i++) jumps.pos[i] = -1;
    for (int64_t i = 0; i < n; i++) {
        uint64_t at = mix(stones[i]) & (jumps.cap - 1);
        while (jumps.pos[at] >= 0) at = (at + 1) & (jumps.cap - 1);
        jumps.pos[at] = stones[i];
        set_init(&jumps.sets[at], 4);
    }
    set_insert(map_get(&jumps, stones[0]), 0);
    int64_t *sizes = NULL, sizes_cap = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t s = stones[i];
        IntSet *here = map_get(&jumps, s);
        int64_t count = 0;
        if (sizes_cap < here->len) {
            sizes_cap = here->len * 2;
            sizes = realloc(sizes, sizes_cap * sizeof(int64_t));
        }
        for (int64_t j = 0; j < here->cap; j++) {
            if (here->keys[j] >= 0) sizes[count++] = here->keys[j];
        }
        for (int64_t j = 0; j < count; j++) {
            int64_t k = sizes[j];
            for (int64_t size = k - 1; size < k + 2; size++) {
                if (size > 0) {
                    IntSet *there = map_get(&jumps, s + size);
                    if (there) set_insert(there, size);
                }
            }
        }
    }
    int crossed = map_get(&jumps, stones[n - 1])->len > 0;
    for (int64_t i = 0; i < jumps.cap; i++) {
        if (jumps.pos[i] >= 0) free(jumps.sets[i].keys);
    }
    free(jumps.pos);
    free(jumps.sets);
    free(sizes);
    return crossed;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(int argc, char **argv) {
    int64_t rivers = argc > 1 ? atoll(argv[1]) : 600;
    int64_t n = 2000;
    int64_t seed = 403, crossed = 0, checksum = 0;
    int64_t *stones = malloc(n * sizeof(int64_t));
    for (int64_t r = 0; r < rivers; r++) {
        stones[0] = 0;
        stones[1] = 1;
        for (int64_t i = 2; i < n; i++) {
            stones[i] = stones[i - 1] + 1 + step(&seed) % 3;
        }
        if (can_cross(stones, n)) {
            crossed++;
            checksum = (checksum * 31 + r + 1) % 1000000007;
        }
    }
    free(stones);
    printf("%lld rivers of %lld stones: %lld crossed, checksum %lld\n", (long long)rivers, (long long)n, (long long)crossed, (long long)checksum);
    return 0;
}
