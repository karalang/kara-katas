// LeetCode #2295: Replace Elements in an Array -- the bench, the ★ arm in
// C. A hash map from each number to its index (open addressing, linear
// probing, backward-shift deletion) finds the one to replace at once; the
// replacement takes over the index.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *keys;
    int64_t *vals;
    uint8_t *used;
    size_t mask;
} Map;

static size_t slot_of(const Map *m, int64_t k) {
    uint64_t h = (uint64_t)k * 0x9E3779B97F4A7C15ull;
    return (size_t)(h >> 20) & m->mask;
}

static void map_init(Map *m, size_t n) {
    size_t cap = 16;
    while (cap < 2 * n) cap <<= 1;
    m->keys = malloc(cap * sizeof(int64_t));
    m->vals = malloc(cap * sizeof(int64_t));
    m->used = calloc(cap, 1);
    m->mask = cap - 1;
}

static void map_free(Map *m) {
    free(m->keys);
    free(m->vals);
    free(m->used);
}

static void map_insert(Map *m, int64_t k, int64_t v) {
    size_t s = slot_of(m, k);
    while (m->used[s] && m->keys[s] != k) s = (s + 1) & m->mask;
    m->used[s] = 1;
    m->keys[s] = k;
    m->vals[s] = v;
}

static int64_t map_remove(Map *m, int64_t k) {
    size_t s = slot_of(m, k);
    while (m->keys[s] != k) {
        if (!m->used[s]) abort();
        s = (s + 1) & m->mask;
    }
    int64_t v = m->vals[s];
    size_t hole = s;
    size_t j = s;
    for (;;) {
        j = (j + 1) & m->mask;
        if (!m->used[j]) break;
        size_t home = slot_of(m, m->keys[j]);
        // move j back into the hole unless its home lies cyclically in (hole, j]
        if (((j - home) & m->mask) >= ((j - hole) & m->mask)) {
            m->keys[hole] = m->keys[j];
            m->vals[hole] = m->vals[j];
            hole = j;
        }
    }
    m->used[hole] = 0;
    return v;
}

static void array_change(const int64_t *nums, size_t n, const int64_t (*ops)[2], size_t m,
                         int64_t *out) {
    memcpy(out, nums, n * sizeof(int64_t));
    Map at;
    map_init(&at, n);
    for (size_t i = 0; i < n; i++) map_insert(&at, out[i], (int64_t)i);
    for (size_t o = 0; o < m; o++) {
        int64_t i = map_remove(&at, ops[o][0]);
        out[i] = ops[o][1];
        map_insert(&at, ops[o][1], i);
    }
    map_free(&at);
}

static int64_t seed = 2295;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t hi = next_random();
    return (hi * 32768 + next_random()) % 1000000 + 1;
}

#define CASES 10
#define N 100000
#define M 100000

int main(void) {
    static int64_t nums[CASES][N];
    static int64_t ops[CASES][M][2];
    static int64_t now[N];
    static int64_t out[N];
    uint8_t *present = malloc(1000001);
    for (int c = 0; c < CASES; c++) {
        memset(present, 0, 1000001);
        size_t len = 0;
        while (len < N) {
            int64_t x = wide();
            if (!present[x]) {
                present[x] = 1;
                nums[c][len++] = x;
            }
        }
        memcpy(now, nums[c], sizeof(now));
        for (int o = 0; o < M; o++) {
            int64_t i = next_random() % N;
            int64_t to = wide();
            while (present[to]) to = to % 1000000 + 1;
            present[now[i]] = 0;
            present[to] = 1;
            ops[c][o][0] = now[i];
            ops[c][o][1] = to;
            now[i] = to;
        }
    }
    free(present);
    int64_t check = 0;
    for (int pass = 0; pass < 3; pass++) {
        for (int c = 0; c < CASES; c++) {
            array_change(nums[c], N, (const int64_t(*)[2])ops[c], M, out);
            for (int i = 0; i < N; i++) check = (check * 31 + out[i]) % 1000000007;
        }
    }
    printf("3 passes over 10 arrays of 10^5 with 10^5 operations: checksum %lld\n",
           (long long)check);
    return 0;
}
