// LeetCode #2420: Find All Good Indices -- the bench, the ★ arm: the run of
// values ending at each index without rising, from the left, and the run
// starting at each index without falling, from the right.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int64_t seed = 2420;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

// The good indices of nums into good; their count.
static int64_t good_indices(const int64_t *nums, int64_t n, int64_t k, int64_t *good) {
    int64_t *falling = malloc(n * sizeof *falling);
    int64_t *rising = malloc(n * sizeof *rising);
    falling[0] = 1;
    for (int64_t i = 1; i < n; i++) falling[i] = nums[i] <= nums[i - 1] ? falling[i - 1] + 1 : 1;
    rising[n - 1] = 1;
    for (int64_t i = n - 2; i >= 0; i--) rising[i] = nums[i] <= nums[i + 1] ? rising[i + 1] + 1 : 1;
    int64_t count = 0;
    for (int64_t i = k; i < n - k; i++)
        if (falling[i - 1] >= k && rising[i + 1] >= k) good[count++] = i;
    free(falling);
    free(rising);
    return count;
}

int main(void) {
    static int64_t arrays[10][N];
    for (int a = 0; a < 10; a++) {
        int down = 1;
        for (int64_t i = 0; i < N; i++) {
            if (i == 0) {
                int64_t hi = next_random();
                arrays[a][i] = 1 + (hi * 32768 + next_random()) % 1000000;
            } else {
                if (next_random() % 60 == 0) down = !down;
                int64_t d = next_random() % 41;
                int64_t v = down ? arrays[a][i - 1] - d : arrays[a][i - 1] + d;
                arrays[a][i] = v < 1 ? 1 : v > 1000000 ? 1000000 : v;
            }
        }
    }
    int64_t *good = malloc(N * sizeof *good);
    int64_t check = 0;
    for (int64_t p = 0; p < 100; p++) {
        for (int64_t a = 0; a < 10; a++) {
            int64_t count = good_indices(arrays[a], N, 1 + (p + a) % 40, good);
            int64_t sum = 0;
            for (int64_t g = 0; g < count; g++) sum += good[g];
            check = (check * 31 + count + sum % 1000003) % 1000000007;
        }
    }
    free(good);
    printf("100 passes over 10 arrays of 10^5 values: checksum %lld\n", (long long)check);
    return 0;
}
