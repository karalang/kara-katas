// LeetCode #2874: Maximum Value of an Ordered Triplet II -- the bench, as
// triplet.kara: 50 arrays of 10^5 values, each answered 20 times by the
// one-pass arm.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t maximum_triplet_value(const int64_t *nums, int64_t n) {
    int64_t best = 0, top = 0, gap = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t v = nums[i];
        if (gap * v > best) best = gap * v;
        if (top - v > gap) gap = top - v;
        if (v > top) top = v;
    }
    return best;
}

static int64_t seed = 2874;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int64_t count = 50, rounds = 20, n = 100000;
    int64_t *arrays = malloc(count * n * sizeof *arrays);
    for (int64_t c = 0; c < count; c++) {
        for (int64_t i = 0; i < n; i++) {
            int64_t v;
            if (c % 2 == 1) {
                v = 1000000 - i * 9 - wide() % 100000;
                if (v < 1) v = 1;
            } else {
                v = wide() % 1000000 + 1;
            }
            arrays[c * n + i] = v;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t best = maximum_triplet_value(arrays + c * n, n);
            total += best;
            check = (check * 31 + best % 1000000007 + r) % 1000000007;
        }
    }
    printf("%lld arrays of %lld, %lld rounds: values total %lld, checksum %lld\n", (long long)count, (long long)n,
           (long long)rounds, (long long)total, (long long)check);
    free(arrays);
    return 0;
}
