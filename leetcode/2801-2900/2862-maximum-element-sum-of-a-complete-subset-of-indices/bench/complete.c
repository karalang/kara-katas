// LeetCode #2862: Maximum Element-Sum of a Complete Subset of Indices --
// the bench: the ★ arm over 200 arrays of 10^4 values up to 10^9,
// LeetCode's most, all drawn first, then each answered 50 times.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t maximum_sum(const int64_t *nums, int64_t n) {
    int64_t best = 0;
    for (int64_t k = 1; k <= n; k++) {
        int64_t sum = 0;
        for (int64_t j = 1; k * j * j <= n; j++) sum += nums[k * j * j - 1];
        if (sum > best) best = sum;
    }
    return best;
}

static int64_t seed = 2862;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int64_t count = 200, rounds = 50, n = 10000;
    int64_t *arrays = malloc(sizeof(int64_t) * count * n);
    for (int64_t i = 0; i < count * n; i++) arrays[i] = wide() % 1000000000 + 1;
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t best = maximum_sum(arrays + c * n, n);
            total += best;
            check = (check * 31 + best % 1000000007 + r) % 1000000007;
        }
    }
    printf("%lld arrays of %lld, %lld rounds: best sums total %lld, checksum %lld\n", (long long)count, (long long)n, (long long)rounds, (long long)total, (long long)check);
    free(arrays);
    return 0;
}
