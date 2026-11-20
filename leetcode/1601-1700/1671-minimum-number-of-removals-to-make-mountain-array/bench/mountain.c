// LeetCode #1671: Minimum Number of Removals to Make Mountain Array -- the
// bench's C mirror: the ★ arm on 300 arrays of 1000 values up to 10^9, one
// raised above the rest, all drawn first.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define ARRAYS 300
#define N 1000
#define MOST 1000000000

static int32_t minimum_mountain_removals(const int32_t *nums, int64_t n) {
    int64_t *up = malloc((size_t)n * sizeof *up);
    int64_t *down = malloc((size_t)n * sizeof *down);
    for (int64_t i = 0; i < n; i++) up[i] = down[i] = 1;
    for (int64_t i = 0; i < n; i++)
        for (int64_t j = 0; j < i; j++)
            if (nums[j] < nums[i] && up[j] + 1 > up[i]) up[i] = up[j] + 1;
    for (int64_t i = n - 1; i >= 0; i--)
        for (int64_t j = i + 1; j < n; j++)
            if (nums[j] < nums[i] && down[j] + 1 > down[i]) down[i] = down[j] + 1;
    int64_t longest = 0;
    for (int64_t i = 1; i < n - 1; i++)
        if (up[i] > 1 && down[i] > 1 && up[i] + down[i] - 1 > longest) longest = up[i] + down[i] - 1;
    free(up);
    free(down);
    return (int32_t)(n - longest);
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1671;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t all[ARRAYS][N];
    for (int a = 0; a < ARRAYS; a++) {
        for (int i = 0; i < N; i++) all[a][i] = (int32_t)((next_random() * 32768 + next_random()) % MOST + 1);
        int64_t peak = next_random() % (N - 2) + 1;
        all[a][peak] = MOST + 1;
    }
    int64_t total = 0, check = 0;
    for (int a = 0; a < ARRAYS; a++) {
        int64_t removed = minimum_mountain_removals(all[a], N);
        total += removed;
        check = (check * 31 + removed) % 1000000007;
    }
    printf("%d arrays of %d values: %lld removals, checksum %lld\n", ARRAYS, N, (long long)total, (long long)check);
    return 0;
}
