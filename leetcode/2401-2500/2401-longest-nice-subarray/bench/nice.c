// LeetCode #2401: Longest Nice Subarray -- the bench, the ★ arm in C: a
// sliding window keeping the OR of its values, values leaving from the
// left by XOR until the new one fits.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 2401;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t longest_nice_subarray(const int64_t *nums, int64_t n) {
    int64_t used = 0, left = 0, best = 0;
    for (int64_t right = 0; right < n; right++) {
        while ((used & nums[right]) != 0) used ^= nums[left++];
        used |= nums[right];
        if (right - left + 1 > best) best = right - left + 1;
    }
    return best;
}

int main(void) {
    int64_t *arrays[20];
    for (int a = 0; a < 20; a++) {
        arrays[a] = malloc(100000 * sizeof(int64_t));
        for (int i = 0; i < 100000; i++) {
            int64_t x = 1LL << (next_random() % 30);
            if (next_random() % 2 == 0) x |= 1LL << (next_random() % 30);
            arrays[a][i] = x;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 20; p++)
        for (int a = 0; a < 20; a++) check = (check * 31 + longest_nice_subarray(arrays[a], 100000) + p) % 1000000007;
    printf("20 passes over 20 arrays of 10^5 values: checksum %lld\n", (long long)check);
    for (int a = 0; a < 20; a++) free(arrays[a]);
    return 0;
}
