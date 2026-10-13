// Benchmark for #462: mirror of min_moves2.kara (the ★ arm: sort, take
// the median) on the same workload. The sort is the C library's qsort.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int compare(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a;
    int64_t y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

// Takes ownership of nums, like the Kāra arm.
static int64_t min_moves2(int64_t *nums, int64_t n) {
    qsort(nums, (size_t)n, sizeof(int64_t), compare);
    int64_t median = nums[n / 2];
    int64_t moves = 0;
    for (int64_t i = 0; i < n; i++) {
        moves += llabs(nums[i] - median);
    }
    free(nums);
    return moves;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t random_number(int64_t *seed) {
    const int64_t spread = 1000000000;
    int64_t a = next_random(seed);
    int64_t b = next_random(seed);
    int64_t c = next_random(seed);
    return ((a * 32768 + b) * 32768 + c) % (2 * spread + 1) - spread;
}

int main(void) {
    const int64_t n = 1000000;
    const int64_t rounds = 10;
    int64_t seed = 462;
    int64_t *nums = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        nums[i] = random_number(&seed);
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t hi = next_random(&seed);
        int64_t lo = next_random(&seed);
        int64_t k = (hi * 65536 + lo) % n;
        nums[k] = random_number(&seed);
        int64_t *copy = malloc(n * sizeof(int64_t));
        memcpy(copy, nums, n * sizeof(int64_t));
        int64_t moves = min_moves2(copy, n);
        total += moves;
        checksum = (checksum * 31 + moves % 1000003) % 1000000007;
    }
    printf("%lld rounds on %lld numbers: %lld moves in all, checksum %lld\n", (long long)rounds,
           (long long)n, (long long)total, (long long)checksum);
    free(nums);
    return 0;
}
