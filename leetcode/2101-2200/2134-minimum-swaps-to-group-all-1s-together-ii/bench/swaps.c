// LeetCode #2134: Minimum Swaps to Group All 1's Together II -- the
// benchmark, the same algorithm as swaps.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t min_swaps(const int64_t *nums, int64_t n) {
    int64_t k = 0;
    for (int64_t i = 0; i < n; i++) k += nums[i];
    int64_t inside = 0;
    for (int64_t i = 0; i < k; i++) inside += nums[i];
    int64_t most = inside;
    for (int64_t i = k; i < n + k; i++) {
        inside += nums[i % n] - nums[(i - k) % n];
        if (inside > most) most = inside;
    }
    return k - most;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2134;
    int64_t *arrays[20];
    for (int64_t a = 0; a < 20; a++) {
        arrays[a] = malloc(N * sizeof(int64_t));
        for (int64_t i = 0; i < N; i++) arrays[a][i] = next_random(&seed) % (a + 2) == 0 ? 1 : 0;
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 10; round++) {
        for (int a = 0; a < 20; a++) {
            int64_t hi = next_random(&seed);
            int64_t at = (hi * 32768 + next_random(&seed)) % N;
            arrays[a][at] = 1 - arrays[a][at];
            int64_t swaps = min_swaps(arrays[a], N);
            total += swaps;
            check = (check * 31 + swaps + round) % 1000000007;
        }
    }
    printf("200 solves: %lld swaps in all, checksum %lld\n", (long long)total, (long long)check);
    for (int a = 0; a < 20; a++) free(arrays[a]);
    return 0;
}
