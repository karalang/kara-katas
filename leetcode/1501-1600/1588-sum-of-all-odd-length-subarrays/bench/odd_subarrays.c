// LeetCode #1588: Sum of All Odd Length Subarrays -- the bench in C,
// mirroring odd_subarrays.kara. Each array is its own malloc.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t sum_odd_length_subarrays(const int32_t *arr, int64_t n) {
    int32_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t through = (i + 1) * (n - i);
        total += (int32_t)((through + 1) / 2) * arr[i];
    }
    return total;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1588;
    int32_t **arrays = malloc(200000 * sizeof(int32_t *));
    int64_t *lens = malloc(200000 * sizeof(int64_t));
    for (int k = 0; k < 200000; k++) {
        int64_t n = next_random(&seed) % 100 + 1;
        int32_t *arr = malloc(n * sizeof(int32_t));
        for (int64_t i = 0; i < n; i++) arr[i] = (int32_t)(next_random(&seed) % 1000 + 1);
        arrays[k] = arr;
        lens[k] = n;
    }
    int64_t check = 0, total = 0;
    for (int k = 0; k < 200000; k++) {
        int64_t answer = sum_odd_length_subarrays(arrays[k], lens[k]);
        total += answer;
        check = (check * 31 + answer + 1) % 1000000007;
    }
    printf("200000 arrays of 1 to 100 values: total %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
