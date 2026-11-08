// LeetCode #1512: Number of Good Pairs -- the bench: 50 arrays of 200000
// numbers from 1 to 100 built once, then each counted four times by the
// ★ arm.
#include <stdio.h>
#include <stdlib.h>

static long num_identical_pairs(const long *nums, long n) {
    long seen[101] = {0};
    long pairs = 0;
    for (long i = 0; i < n; i++) {
        pairs += seen[nums[i]];
        seen[nums[i]] += 1;
    }
    return pairs;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    long seed = 1512;
    long *arrays = malloc(sizeof(long) * 50 * 200000);
    for (long a = 0; a < 50; a++)
        for (long i = 0; i < 200000; i++) arrays[a * 200000 + i] = next_random(&seed) % 100 + 1;
    long check = 0;
    for (int r = 0; r < 4; r++)
        for (long a = 0; a < 50; a++)
            check = (check * 31 + num_identical_pairs(arrays + a * 200000, 200000) + 1) % 1000000007;
    printf("200 counts over 50 arrays of 200000 numbers: checksum %ld\n", check);
    free(arrays);
    return 0;
}
