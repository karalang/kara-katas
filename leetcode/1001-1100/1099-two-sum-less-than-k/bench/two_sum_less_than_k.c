// Benchmark: LeetCode #1099 Two Sum Less Than K -- C mirror of
// two_sum_less_than_k.kara: the ★ arm, sorting and two pointers, over 64
// arrays of 100 values built once, 400 rounds each changing one value per
// array and asking for 8 values of k. Each call copies the array to a
// fresh malloc'd buffer and sorts it with qsort, as Kāra clones and sorts.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t two_sum_less_than_k(const int64_t *nums, int64_t n, int64_t k) {
    int64_t *v = malloc(n * sizeof(int64_t));
    memcpy(v, nums, n * sizeof(int64_t));
    qsort(v, n, sizeof(int64_t), cmp);
    int64_t best = -1;
    int64_t lo = 0, hi = n - 1;
    while (lo < hi) {
        int64_t sum = v[lo] + v[hi];
        if (sum < k) {
            if (sum > best) best = sum;
            lo++;
        } else {
            hi--;
        }
    }
    free(v);
    return best;
}

static int64_t seed = 1099;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t arrays[64][100];
    for (int j = 0; j < 64; j++)
        for (int i = 0; i < 100; i++) arrays[j][i] = next_random() % 1000 + 1;
    int64_t found = 0, check = 0;
    for (int64_t round = 0; round < 400; round++) {
        for (int64_t j = 0; j < 64; j++) {
            int64_t at = (round * 7 + j * 13) % 100;
            arrays[j][at] = (arrays[j][at] + round * 31) % 1000 + 1;
            for (int64_t q = 0; q < 8; q++) {
                int64_t k = (round * 97 + j * 61 + q * 251) % 2000 + 1;
                int64_t best = two_sum_less_than_k(arrays[j], 100, k);
                if (best >= 0) found++;
                check = (check * 31 + best + 1) % 1000000007;
            }
        }
    }
    printf("400 rounds over 64 arrays of 100 values: %lld of 204800 with a pair, checksum %lld\n", (long long)found,
           (long long)check);
    return 0;
}
