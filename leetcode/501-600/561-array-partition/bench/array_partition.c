// Benchmark for #561: C mirror of the ★ arm (sort, then every other
// number); see array_partition.kara. The copy is `malloc`'d and sorted
// with the C library's `qsort`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int compare(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a;
    int64_t y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t array_pair_sum(int64_t *nums, size_t n) {
    qsort(nums, n, sizeof(int64_t), compare);
    int64_t sum = 0;
    for (size_t i = 0; i < n; i += 2) {
        sum += nums[i];
    }
    free(nums);
    return sum;
}

// ---- benchmark --------------------------------------------------------------

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 100;
    const int64_t n = 20000;
    const int64_t rounds = 50;
    int64_t seed = 561;
    int64_t **arrays = malloc(count * sizeof(int64_t *));
    for (int64_t a = 0; a < count; a++) {
        arrays[a] = malloc(n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            arrays[a][i] = step(&seed) % 20001 - 10000;
        }
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int64_t g = 0; g < count; g++) {
            int64_t *copy = malloc(n * sizeof(int64_t));
            memcpy(copy, arrays[(round * 7 + g) % count], n * sizeof(int64_t));
            int64_t s = array_pair_sum(copy, (size_t)n);
            total += s;
            checksum = (checksum * 31 + s + 1000000000) % 1000000007;
        }
    }
    printf("%lld arrays of %lld, %lld rounds: total %lld, checksum %lld\n",
           (long long)count, (long long)n, (long long)rounds, (long long)total, (long long)checksum);
    for (int64_t a = 0; a < count; a++) {
        free(arrays[a]);
    }
    free(arrays);
    return 0;
}
