// Benchmark for #396: mirror of rotate_function.kara (one rotation from the last).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t max_rotate_function(const int64_t *nums, int64_t n) {
    int64_t sum = 0, f = 0;
    for (int64_t i = 0; i < n; i++) {
        sum += nums[i];
        f += i * nums[i];
    }
    int64_t best = f;
    for (int64_t k = 1; k < n; k++) {
        f = f + sum - n * nums[n - k];
        if (f > best) best = f;
    }
    return best;
}

static int64_t seed = 396;

static int64_t step(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(int argc, char **argv) {
    int64_t windows = argc > 1 ? atoll(argv[1]) : 2000;
    int64_t *pool = malloc(1000000 * sizeof(int64_t));
    for (int i = 0; i < 1000000; i++) {
        pool[i] = step() % 201 - 100;
    }
    const int64_t m = 1000000007;
    int64_t total = 0, checksum = 0;
    for (int64_t w = 0; w < windows; w++) {
        int64_t hi = step();
        int64_t a = (hi * 32768 + step()) % (1000000 - 100000);
        int64_t r = max_rotate_function(pool + a, 100000);
        total += r;
        checksum = (checksum * 31 + r % m + m) % m;
    }
    printf("%lld windows: total %lld, checksum %lld\n", (long long)windows, (long long)total, (long long)checksum);
    free(pool);
    return 0;
}
