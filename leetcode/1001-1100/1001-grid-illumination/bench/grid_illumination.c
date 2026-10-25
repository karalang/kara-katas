// Benchmark: LeetCode #1001 Grid Illumination -- the ★ arm, counts per
// line in hash maps, on grids of 10^9 by 10^9 with 20000 lamps and 20000
// queries, LeetCode's largest. Mirrors grid_illumination.kara, .rs, .py
// and go-seq/. C has no hash map, so each map here is a small open-
// addressing table with linear probing; a count that falls to 0, and a
// lamp turned off, keep their slot with the value 0.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *keys, *vals;
    uint8_t *used;
    int64_t cap;
} Table;

static void table_init(Table *t, int64_t at_least) {
    t->cap = 16;
    while (t->cap < 2 * at_least) t->cap *= 2;
    t->keys = malloc(sizeof(int64_t) * (size_t)t->cap);
    t->vals = malloc(sizeof(int64_t) * (size_t)t->cap);
    t->used = calloc((size_t)t->cap, 1);
}

static void table_free(Table *t) {
    free(t->keys);
    free(t->vals);
    free(t->used);
}

static int64_t slot(const Table *t, int64_t key) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ULL;
    int64_t i = (int64_t)(h >> 20) & (t->cap - 1);
    while (t->used[i] && t->keys[i] != key) i = (i + 1) & (t->cap - 1);
    return i;
}

static int64_t get(const Table *t, int64_t key) {
    int64_t i = slot(t, key);
    return t->used[i] ? t->vals[i] : 0;
}

static void add(Table *t, int64_t key, int64_t d) {
    int64_t i = slot(t, key);
    if (!t->used[i]) {
        t->used[i] = 1;
        t->keys[i] = key;
        t->vals[i] = 0;
    }
    t->vals[i] += d;
}

static void grid_illumination(int64_t n, int64_t (*lamps)[2], int64_t nl, int64_t (*queries)[2],
                              int64_t nq, int64_t *ans) {
    Table on, rows, cols, diags, antis;
    table_init(&on, nl);
    table_init(&rows, nl);
    table_init(&cols, nl);
    table_init(&diags, nl);
    table_init(&antis, nl);
    for (int64_t k = 0; k < nl; k++) {
        int64_t r = lamps[k][0], c = lamps[k][1];
        if (get(&on, r * n + c) == 0) {
            add(&on, r * n + c, 1);
            add(&rows, r, 1);
            add(&cols, c, 1);
            add(&diags, r - c, 1);
            add(&antis, r + c, 1);
        }
    }
    for (int64_t q = 0; q < nq; q++) {
        int64_t r = queries[q][0], c = queries[q][1];
        ans[q] = get(&rows, r) > 0 || get(&cols, c) > 0 || get(&diags, r - c) > 0 ||
                 get(&antis, r + c) > 0;
        for (int64_t i = r - 1; i < r + 2; i++)
            for (int64_t j = c - 1; j < c + 2; j++)
                if (i >= 0 && i < n && j >= 0 && j < n && get(&on, i * n + j) > 0) {
                    add(&on, i * n + j, -1);
                    add(&rows, i, -1);
                    add(&cols, j, -1);
                    add(&diags, i - j, -1);
                    add(&antis, i + j, -1);
                }
    }
    table_free(&on);
    table_free(&rows);
    table_free(&cols);
    table_free(&diags);
    table_free(&antis);
}

static int64_t seed = 1001;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t big_random(void) {
    int64_t hi = next_random();
    return hi * 32768 + next_random();
}

static int64_t lamps[20][20000][2], queries[20][20000][2], ans[20000];

int main(void) {
    const int64_t rounds = 1, n = 1000000000;
    // 20 cases, each with 20000 lamps in a window of 100000 by 100000
    // cells at a random place in the grid, and 20000 queries, half of them
    // anywhere in the window and half on or beside a random lamp
    for (int t = 0; t < 20; t++) {
        int64_t top = 1 + big_random() % (n - 100002);
        int64_t left = 1 + big_random() % (n - 100002);
        for (int k = 0; k < 20000; k++) {
            int64_t r = top + big_random() % 100000;
            lamps[t][k][0] = r;
            lamps[t][k][1] = left + big_random() % 100000;
        }
        for (int q = 0; q < 20000; q++) {
            if (q % 2 == 0) {
                int64_t r = top + big_random() % 100000;
                queries[t][q][0] = r;
                queries[t][q][1] = left + big_random() % 100000;
            } else {
                int64_t *lamp = lamps[t][next_random() % 20000];
                int64_t r = lamp[0] + next_random() % 3 - 1;
                queries[t][q][0] = r;
                queries[t][q][1] = lamp[1] + next_random() % 3 - 1;
            }
        }
    }
    int64_t lit = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < 20; i++) {
            int64_t k = (r + i) % 20;
            grid_illumination(n, lamps[k], 20000, queries[k], 20000, ans);
            for (int q = 0; q < 20000; q++) {
                lit += ans[q];
                check = (check * 31 + ans[q] + 1) % 1000000007;
            }
        }
    }
    printf("%lld rounds over 20 grids of 20000 lamps and 20000 queries: %lld lit, checksum %lld\n",
           (long long)rounds, (long long)lit, (long long)check);
    return 0;
}
