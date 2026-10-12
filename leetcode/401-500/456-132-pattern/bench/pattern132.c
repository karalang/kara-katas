// Benchmark for #456: mirror of pattern132.kara (the ★ arm, one stack
// from the right) on the same workload.
#include <inttypes.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static bool find132pattern(const int64_t *nums, int64_t n) {
    int64_t *stack = malloc(n * sizeof(int64_t));
    int64_t len = 0;
    int64_t third = INT64_MIN;
    bool found = false;
    for (int64_t i = n - 1; i >= 0; i--) {
        if (nums[i] < third) {
            found = true;
            break;
        }
        while (len > 0 && stack[len - 1] < nums[i]) {
            third = stack[--len];
        }
        stack[len++] = nums[i];
    }
    free(stack);
    return found;
}

// ---- benchmark --------------------------------------------------------

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t arrays = 10;
    const int64_t n = 1000000;
    const int64_t rounds = 5;
    int64_t seed = 456;
    int64_t *all[10];
    for (int64_t a = 0; a < arrays; a++) {
        all[a] = malloc(n * sizeof(int64_t));
        int64_t len = 0;
        int64_t top = 1000000000;
        while (len < n) {
            int64_t run = 1 + next_random(&seed) % 1000;
            if (run > n - len) {
                run = n - len;
            }
            int64_t low = top - run * 10 - 1 - next_random(&seed) % 100;
            for (int64_t t = 0; t < run; t++) {
                all[a][len++] = low + t * 10 + next_random(&seed) % 10;
            }
            top = low;
        }
    }
    int64_t found = 0;
    int64_t checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t a = 0; a < arrays; a++) {
            int64_t hi = next_random(&seed);
            int64_t lo = next_random(&seed);
            int64_t at = (hi * 65536 + lo) % n;
            int64_t old = all[a][at];
            hi = next_random(&seed);
            lo = next_random(&seed);
            int64_t value = (hi * 65536 + lo) % 2000000001 - 1000000000;
            if (next_random(&seed) % 2 == 0) {
                all[a][at] = value;
            }
            bool has = find132pattern(all[a], n);
            all[a][at] = old;
            if (has) {
                found += 1;
            }
            checksum = (checksum * 31 + (has ? at + 1 : 0)) % 1000000007;
        }
    }
    printf("%" PRId64 " rounds on %" PRId64 " arrays of %" PRId64 ": %" PRId64 " with the pattern, checksum %" PRId64
           "\n",
           rounds, arrays, n, found, checksum);
    for (int64_t a = 0; a < arrays; a++) {
        free(all[a]);
    }
    return 0;
}
