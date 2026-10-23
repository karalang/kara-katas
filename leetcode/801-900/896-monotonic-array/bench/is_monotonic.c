// LeetCode #896 bench: the ★ arm (one pass, two flags) over 16 arrays of
// 100,000 numbers, LeetCode's largest, built once as random walks, half
// rising and half falling. Each of 2,000 rounds sets one random place of
// one array to the number before it, which keeps the array monotonic, or
// in every other round to a random number, asks whether the array is
// monotonic, and puts the number back. The same algorithm as
// is_monotonic.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int is_monotonic(const int64_t *nums, int64_t n) {
    int rising = 1, falling = 1;
    for (int64_t i = 1; i < n; i++) {
        if (nums[i] > nums[i - 1]) falling = 0;
        if (nums[i] < nums[i - 1]) rising = 0;
    }
    return rising || falling;
}

static int64_t seed = 896;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t *arrays[16];
    for (int k = 0; k < 16; k++) {
        int64_t *nums = malloc(100000 * sizeof(int64_t));
        int64_t x = k % 2 == 0 ? -100000 : 100000;
        for (int i = 0; i < 100000; i++) {
            nums[i] = x;
            int64_t step = next_random() % 2;
            x = k % 2 == 0 ? x + step : x - step;
        }
        arrays[k] = nums;
    }
    int64_t monotonic = 0, check = 0;
    for (int r = 0; r < 2000; r++) {
        int64_t a = next_random() % 16;
        int64_t p = next_random() * 32768;
        p = (p + next_random()) % 100000;
        int64_t random = next_random() * 32768;
        random = (random + next_random()) % 200001 - 100000;
        int64_t old = arrays[a][p];
        int64_t value = (next_random() % 2 == 0 && p > 0) ? arrays[a][p - 1] : random;
        arrays[a][p] = value;
        int got = is_monotonic(arrays[a], 100000);
        arrays[a][p] = old;
        if (got) monotonic++;
        check = (check * 131 + p * 2 + (got ? 1 : 0)) % 1000000007;
    }
    printf("2000 rounds over 16 arrays of 100000 numbers: %lld monotonic, checksum %lld\n",
           (long long)monotonic, (long long)check);
    for (int k = 0; k < 16; k++) free(arrays[k]);
    return 0;
}
