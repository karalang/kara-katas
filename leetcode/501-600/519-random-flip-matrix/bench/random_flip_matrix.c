// Benchmark for #519: C mirror of the ★ arm (a shuffle kept in a hash
// map); see random_flip_matrix.kara. C has no map of its own, so this
// is an open-addressing table with linear probing, a fresh one for
// every grid, as the ★ arm's `Map.new()`. A grid sees at most 999 flips
// between resets, so 4,096 slots never fill; a reset empties only the
// slots in use.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define SLOTS 4096

typedef struct {
    int64_t seed;
} Draw;

static int64_t step(Draw *d) {
    d->seed = (d->seed * 1103515245 + 12345) % 2147483648LL;
    return d->seed / 65536;
}

// Uniform in [0, n) for n up to 2^30: 30 random bits, drawn again when
// they land in the last, incomplete run of n.
static int64_t below(Draw *d, int64_t n) {
    int64_t limit = 1073741824LL / n * n;
    for (;;) {
        int64_t high = step(d);
        int64_t low = step(d);
        int64_t r = high * 32768 + low;
        if (r < limit) return r % n;
    }
}

typedef struct {
    int64_t m, n, free;
    int64_t *keys, *vals;
    unsigned char *full;
    int64_t *used;  // the slots in use, for a reset
    int64_t count;
    Draw draw;
} Solution;

static Solution solution_new(int64_t m, int64_t n, int64_t seed) {
    Solution s = {m, n, m * n, malloc(SLOTS * sizeof(int64_t)), malloc(SLOTS * sizeof(int64_t)),
                  calloc(SLOTS, 1), malloc(SLOTS * sizeof(int64_t)), 0, {seed}};
    return s;
}

static void solution_free(Solution *s) {
    free(s->keys);
    free(s->vals);
    free(s->full);
    free(s->used);
}

static uint64_t slot_of(int64_t key) {
    return ((uint64_t)key * 0x9E3779B97F4A7C15ULL) >> 52;
}

// What slot `i` of the shuffled cells holds.
static int64_t at(const Solution *s, int64_t i) {
    for (uint64_t h = slot_of(i);; h = (h + 1) & (SLOTS - 1)) {
        if (!s->full[h]) return i;
        if (s->keys[h] == i) return s->vals[h];
    }
}

static void set(Solution *s, int64_t key, int64_t val) {
    uint64_t h = slot_of(key);
    while (s->full[h] && s->keys[h] != key) h = (h + 1) & (SLOTS - 1);
    if (!s->full[h]) {
        s->full[h] = 1;
        s->keys[h] = key;
        s->used[s->count++] = (int64_t)h;
    }
    s->vals[h] = val;
}

static void flip(Solution *s, int64_t *row, int64_t *col) {
    int64_t r = below(&s->draw, s->free);
    s->free -= 1;
    int64_t cell = at(s, r);
    int64_t last = at(s, s->free);
    set(s, r, last);
    *row = cell / s->n;
    *col = cell % s->n;
}

static void reset(Solution *s) {
    for (int64_t i = 0; i < s->count; i++) s->full[s->used[i]] = 0;
    s->count = 0;
    s->free = s->m * s->n;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // 10,000 grids of up to 10,000 by 10,000, 1,000 calls on each: a
    // reset one time in a hundred and whenever the grid is full, else a
    // flip.
    int64_t seed = 519, checksum = 0, grids = 10000;
    for (int64_t g = 0; g < grids; g++) {
        int64_t high = next_random(&seed);
        int64_t m = 1 + (high * 32768 + next_random(&seed)) % 10000;
        high = next_random(&seed);
        int64_t n = 1 + (high * 32768 + next_random(&seed)) % 10000;
        Solution s = solution_new(m, n, g);
        int64_t free_cells = m * n;
        for (int i = 0; i < 1000; i++) {
            if (free_cells == 0 || next_random(&seed) % 100 == 0) {
                reset(&s);
                free_cells = m * n;
            } else {
                int64_t row, col;
                flip(&s, &row, &col);
                free_cells -= 1;
                checksum = (checksum * 31 + row * 10000 + col) % 1000000007;
            }
        }
        solution_free(&s);
    }
    printf("%lld grids, 1000 calls each: checksum %lld\n", (long long)grids, (long long)checksum);
    return 0;
}
