// LeetCode #1636: Sort Array by Increasing Frequency -- the bench's C
// mirror: the ★ arm on 50000 random arrays of 100 values from -100 to 100,
// all drawn first, with an open-addressing hash map written out for the
// counts, looked up on every comparison as the other languages' keys are.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { ARRAYS = 50000, N = 100, CAP = 256 };

typedef struct {
    int32_t keys[CAP];
    int64_t values[CAP];
    char used[CAP];
} Map;

static size_t slot(const Map *m, int32_t key) {
    uint64_t h = (uint64_t)(int64_t)key * 0x9E3779B97F4A7C15ull;
    size_t i = (size_t)(h >> 32) & (CAP - 1);
    while (m->used[i] && m->keys[i] != key) i = (i + 1) & (CAP - 1);
    return i;
}

static const Map *counts;

static int by_key(const void *x, const void *y) {
    int32_t a = *(const int32_t *)x, b = *(const int32_t *)y;
    int64_t ca = counts->values[slot(counts, a)], cb = counts->values[slot(counts, b)];
    if (ca != cb) return ca < cb ? -1 : 1;
    return (a < b) - (a > b);
}

static void frequency_sort(const int32_t *nums, int32_t *sorted) {
    Map *count = calloc(1, sizeof(Map));
    for (int i = 0; i < N; i++) {
        size_t s = slot(count, nums[i]);
        if (!count->used[s]) {
            count->used[s] = 1;
            count->keys[s] = nums[i];
            count->values[s] = 0;
        }
        count->values[s]++;
    }
    memcpy(sorted, nums, sizeof(int32_t) * N);
    counts = count;
    qsort(sorted, N, sizeof(int32_t), by_key);
    free(count);
}

static int64_t seed = 1636;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t arrays[ARRAYS][N];
    int32_t sorted[N];
    for (int a = 0; a < ARRAYS; a++)
        for (int i = 0; i < N; i++) arrays[a][i] = (int32_t)(next_random() % 201 - 100);
    int64_t check = 0;
    for (int a = 0; a < ARRAYS; a++) {
        frequency_sort(arrays[a], sorted);
        for (int i = 0; i < N; i++) check = (check * 31 + sorted[i] + 1000) % 1000000007;
    }
    printf("50000 arrays of 100 values: checksum %lld\n", (long long)check);
    return 0;
}
