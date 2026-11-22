// LeetCode #2871: Split Array Into Maximum Number of Subarrays -- the
// bench, as split.kara: 50 arrays of 10^5 values, each answered 10 times
// by the greedy arm.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t max_subarrays(const int64_t *nums, int64_t n) {
    int64_t parts = 0, running = -1;
    for (int64_t i = 0; i < n; i++) {
        running &= nums[i];
        if (running == 0) {
            parts++;
            running = -1;
        }
    }
    return parts > 1 ? parts : 1;
}

static int64_t seed = 2871;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int64_t count = 50, rounds = 10, n = 100000;
    int64_t *arrays = malloc(count * n * sizeof *arrays);
    for (int64_t c = 0; c < count; c++) {
        for (int64_t i = 0; i < n; i++) {
            if (c % 2 == 0) {
                arrays[c * n + i] = wide() % 1000001;
            } else {
                int64_t a = wide();
                arrays[c * n + i] = (a | wide()) % 1000001;
            }
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t parts = max_subarrays(arrays + c * n, n);
            total += parts;
            check = (check * 31 + parts + r) % 1000000007;
        }
    }
    printf("%lld arrays of %lld, %lld rounds: %lld subarrays, checksum %lld\n", (long long)count, (long long)n,
           (long long)rounds, (long long)total, (long long)check);
    free(arrays);
    return 0;
}
