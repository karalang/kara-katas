// Benchmark: LeetCode #945 Minimum Increment to Make Array Unique -- the
// ★ arm, sorted and raised, on arrays of 100000 values, LeetCode's
// longest. Mirrors min_increment_for_unique.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100000
#define COUNT 20

static int cmp_i64(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t min_increment_for_unique(const int64_t *nums, int64_t n) {
    int64_t *a = malloc(sizeof(int64_t) * (size_t)n);
    memcpy(a, nums, sizeof(int64_t) * (size_t)n);
    qsort(a, (size_t)n, sizeof(int64_t), cmp_i64);
    int64_t moves = 0, floor = -1;
    for (int64_t i = 0; i < n; i++) {
        int64_t end = a[i] > floor + 1 ? a[i] : floor + 1;
        moves += end - a[i];
        floor = end;
    }
    free(a);
    return moves;
}

static int64_t seed = 945;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t arrays[COUNT][N];

int main(void) {
    const int64_t rounds = 5, count = COUNT, n = N;
    for (int64_t c = 0; c < count; c++) {
        int64_t range = 70001 + next_random() * 4 % 30001;
        for (int64_t i = 0; i < n; i++) {
            int64_t wide = next_random() * 32768;
            wide += next_random();
            arrays[c][i] = wide % range;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < count; i++) {
            int64_t m = min_increment_for_unique(arrays[(r + i) % count], n);
            total += m;
            check = (check * 1000003 + m) % 1000000007;
        }
    }
    printf("%lld rounds over %lld arrays of %lld values: %lld moves, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)n, (long long)total, (long long)check);
    return 0;
}
