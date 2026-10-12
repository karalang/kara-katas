// Benchmark for #453: mirror of min_moves.kara (the ★ arm, sum minus n
// times the minimum) on the same workload.
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t min_moves(const int64_t *nums, int64_t n) {
    int64_t smallest = nums[0];
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        if (nums[i] < smallest) {
            smallest = nums[i];
        }
        total += nums[i];
    }
    return total - n * smallest;
}

// ---- benchmark --------------------------------------------------------

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t random_value(int64_t *seed) {
    int64_t hi = next_random(seed);
    int64_t lo = next_random(seed);
    return (hi * 65536 + lo) % 2000000001 - 1000000000;
}

int main(void) {
    const int64_t arrays = 10;
    const int64_t n = 1000000;
    const int64_t rounds = 20;
    int64_t seed = 453;
    int64_t *all[10];
    for (int64_t a = 0; a < arrays; a++) {
        all[a] = malloc(n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            all[a][i] = random_value(&seed);
        }
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t a = 0; a < arrays; a++) {
            int64_t hi = next_random(&seed);
            int64_t lo = next_random(&seed);
            int64_t at = (hi * 65536 + lo) % n;
            all[a][at] = random_value(&seed);
            int64_t moves = min_moves(all[a], n);
            total += moves;
            checksum = (checksum * 31 + moves % 1000000007) % 1000000007;
        }
    }
    printf("%" PRId64 " rounds on %" PRId64 " arrays of %" PRId64 ": %" PRId64 " moves, checksum %" PRId64 "\n",
           rounds, arrays, n, total, checksum);
    for (int64_t a = 0; a < arrays; a++) {
        free(all[a]);
    }
    return 0;
}
