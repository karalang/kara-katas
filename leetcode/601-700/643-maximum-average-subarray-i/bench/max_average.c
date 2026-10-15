// Benchmark for #643: mirror of max_average.kara (the ★ arm: a sliding
// sum) on the same workload.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static double find_max_average(const int64_t *nums, int64_t n, int64_t k) {
    int64_t sum = 0;
    for (int64_t i = 0; i < k; i++) {
        sum += nums[i];
    }
    int64_t best = sum;
    for (int64_t i = k; i < n; i++) {
        sum += nums[i] - nums[i - k];
        if (sum > best) {
            best = sum;
        }
    }
    return (double)best / (double)k;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 643;
    int64_t n = 100000;
    int64_t *arrays[20];
    for (int a = 0; a < 20; a++) {
        arrays[a] = malloc((size_t)n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            arrays[a][i] = next_random(&seed) % 20001 - 10000;
        }
    }
    int64_t rounds = 4000;
    double total = 0.0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t k = 1 + (r * 7919) % 100000;
        total += find_max_average(arrays[r % 20], n, k);
    }
    printf("%lld rounds over 20 arrays of 100000 values: answers adding to %.5f\n", (long long)rounds, total);
    for (int a = 0; a < 20; a++) {
        free(arrays[a]);
    }
    return 0;
}
