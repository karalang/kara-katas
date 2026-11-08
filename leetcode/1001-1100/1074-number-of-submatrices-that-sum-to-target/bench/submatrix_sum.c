// LeetCode #1074: Number of Submatrices That Sum to Target -- the
// benchmark's C mirror of submatrix_sum.kara: the same row pairs and a map
// of running totals, a fresh open-addressing table for each band (C has no
// standard map; its hash is a multiply, not SipHash), over 30 matrices of
// 100 by 100 built once, each counted for three targets.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *keys, *vals;
    unsigned char *used;
    int64_t cap;
} map;

static map map_new(int64_t cap) {
    map t = {malloc(cap * sizeof(int64_t)), malloc(cap * sizeof(int64_t)), calloc(cap, 1), cap};
    return t;
}

static void map_free(map *t) {
    free(t->keys);
    free(t->vals);
    free(t->used);
}

static int64_t slot(const map *t, int64_t key) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ull;
    int64_t i = (int64_t)(h >> 32) & (t->cap - 1);
    while (t->used[i] && t->keys[i] != key) i = (i + 1) & (t->cap - 1);
    return i;
}

static int64_t map_get(const map *t, int64_t key) {
    int64_t i = slot(t, key);
    return t->used[i] ? t->vals[i] : 0;
}

static void map_put(map *t, int64_t key, int64_t val) {
    int64_t i = slot(t, key);
    t->used[i] = 1;
    t->keys[i] = key;
    t->vals[i] = val;
}

static int64_t num_submatrix_sum_target(int64_t **matrix, int64_t m, int64_t n, int64_t target) {
    int64_t count = 0;
    int64_t cap = 1;
    while (cap < 2 * (n + 1)) cap *= 2;
    int64_t *column = malloc(n * sizeof(int64_t));
    for (int64_t top = 0; top < m; top++) {
        for (int64_t c = 0; c < n; c++) column[c] = 0;
        for (int64_t bottom = top; bottom < m; bottom++) {
            for (int64_t c = 0; c < n; c++) column[c] += matrix[bottom][c];
            map seen = map_new(cap);
            map_put(&seen, 0, 1);
            int64_t total = 0;
            for (int64_t c = 0; c < n; c++) {
                total += column[c];
                count += map_get(&seen, total - target);
                map_put(&seen, total, map_get(&seen, total) + 1);
            }
            map_free(&seen);
        }
    }
    free(column);
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1074;
    int64_t **matrices[30];
    for (int k = 0; k < 30; k++) {
        matrices[k] = malloc(100 * sizeof(int64_t *));
        for (int r = 0; r < 100; r++) {
            matrices[k][r] = malloc(100 * sizeof(int64_t));
            for (int c = 0; c < 100; c++) matrices[k][r][c] = next_random(&seed) % 7 - 3;
        }
    }
    int64_t targets[3] = {-5, 0, 7};
    int64_t total = 0, check = 0;
    for (int k = 0; k < 30; k++) {
        for (int t = 0; t < 3; t++) {
            int64_t x = num_submatrix_sum_target(matrices[k], 100, 100, targets[t]);
            total += x;
            check = (check * 31 + x) % 1000000007;
        }
    }
    printf("90 calls: %lld submatrices, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
