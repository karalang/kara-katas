// LeetCode #1480: Running Sum of 1d Array -- bench, C mirror of
// running_sum.kara. Each call writes into a malloc'ed array of its own, as
// the Kāra and Rust ones grow a new list.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t *running_sum(const int32_t *nums, int64_t n) {
    int32_t *sums = malloc(sizeof(int32_t) * n);
    int32_t sum = 0;
    for (int64_t i = 0; i < n; i++) {
        sum += nums[i];
        sums[i] = sum;
    }
    return sums;
}

static int64_t seed = 1480;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int32_t **arrays = malloc(sizeof(int32_t *) * 1000);
    for (int p = 0; p < 1000; p++) {
        arrays[p] = malloc(sizeof(int32_t) * 1000);
        for (int i = 0; i < 1000; i++) {
            int64_t hi = next_random();
            arrays[p][i] = (int32_t)((hi * 32768 + next_random()) % 2000001 - 1000000);
        }
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 200; pass++) {
        for (int p = 0; p < 1000; p++) {
            arrays[p][check % 1000] = (int32_t)((check / 7) % 2000001 - 1000000);
            int32_t *sums = running_sum(arrays[p], 1000);
            int64_t s = 0;
            for (int64_t j = 0; j < 1000; j++) s += (int64_t)sums[j] * (j + 1);
            free(sums);
            check = (check * 31 + s % 1000000007 + 1000000007 + pass) % 1000000007;
        }
    }
    printf("200 passes over 1000 arrays of 1000 values: checksum %lld\n", (long long)check);
    for (int p = 0; p < 1000; p++) free(arrays[p]);
    free(arrays);
    return 0;
}
