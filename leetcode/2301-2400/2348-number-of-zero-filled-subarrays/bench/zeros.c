// LeetCode #2348: Number of Zero-Filled Subarrays -- the bench, the ★ arm
// in C: the length of the run of zeros ending at each place, summed.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t zero_filled_subarray(const int64_t *nums, int64_t n) {
    int64_t run = 0, total = 0;
    for (int64_t i = 0; i < n; i++) {
        if (nums[i] == 0)
            run += 1;
        else
            run = 0;
        total += run;
    }
    return total;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245LL + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // array a holds a value that is not zero with a chance of 1 in a + 2
    int64_t seed = 2348;
    int64_t *arrays[10];
    for (int64_t a = 0; a < 10; a++) {
        arrays[a] = malloc(100000 * sizeof(int64_t));
        for (int64_t i = 0; i < 100000; i++) {
            int64_t r = next_random(&seed);
            arrays[a][i] = r % (a + 2) == 0 ? r + 1 : 0;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 60; p++)
        for (int a = 0; a < 10; a++) check = (check * 31 + zero_filled_subarray(arrays[a], 100000) + p) % 1000000007;
    printf("60 passes over 10 arrays of 10^5 values: checksum %lld\n", (long long)check);
    for (int a = 0; a < 10; a++) free(arrays[a]);
    return 0;
}
