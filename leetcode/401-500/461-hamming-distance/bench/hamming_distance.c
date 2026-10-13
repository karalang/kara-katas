// Benchmark for #461: mirror of hamming_distance.kara (the ★ arm, clearing
// the lowest set bit) on the same workload.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t hamming_distance(int64_t x, int64_t y) {
    int64_t z = x ^ y;
    int64_t count = 0;
    while (z != 0) {
        z &= z - 1;
        count += 1;
    }
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t random31(int64_t *seed) {
    int64_t a = next_random(seed);
    int64_t b = next_random(seed);
    int64_t c = next_random(seed);
    return ((a * 32768 + b) * 2 + c % 2) % 2147483648LL;
}

int main(void) {
    const int64_t n = 1000000;
    const int64_t rounds = 20;
    int64_t seed = 461;
    int64_t *nums = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        nums[i] = random31(&seed);
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t hi = next_random(&seed);
        int64_t lo = next_random(&seed);
        int64_t k = (hi * 65536 + lo) % n;
        nums[k] = random31(&seed);
        int64_t sum = 0;
        for (int64_t i = 1; i < n; i++) {
            sum += hamming_distance(nums[i - 1], nums[i]);
        }
        total += sum;
        checksum = (checksum * 31 + sum) % 1000000007;
    }
    printf("%lld rounds on %lld numbers: total distance %lld, checksum %lld\n", (long long)rounds,
           (long long)n, (long long)total, (long long)checksum);
    free(nums);
    return 0;
}
