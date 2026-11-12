// LeetCode #1133: Largest Unique Number -- the bench in C, the same
// algorithm and workload as largest_unique_number.kara: each array
// allocated by itself, a fixed array of 1001 counts per call, the same 256
// arrays of 2000 values and 1000 rounds.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t largest_unique_number(const int64_t *nums, int64_t n) {
    int64_t count[1001] = {0};
    for (int64_t i = 0; i < n; i++) count[nums[i]] += 1;
    for (int64_t v = 1000; v >= 0; v--) {
        if (count[v] == 1) return v;
    }
    return -1;
}

static int64_t seed = 1133;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t *arrays[256];
    for (int j = 0; j < 256; j++) {
        arrays[j] = malloc(2000 * sizeof(int64_t));
        for (int i = 0; i < 2000; i++) arrays[j][i] = next_random() % 1001;
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 1000; round++) {
        for (int64_t j = 0; j < 256; j++) {
            int64_t at = (round * 7919 + j * 104729) % 2000;
            arrays[j][at] = (arrays[j][at] * 7 + 13) % 1001;
            int64_t r = largest_unique_number(arrays[j], 2000);
            total += r;
            check = (check * 31 + r + 1) % 1000000007;
        }
    }
    printf("1000 rounds over 256 arrays of 2000 values: answers total %lld, checksum %lld\n",
           (long long)total, (long long)check);
    for (int j = 0; j < 256; j++) free(arrays[j]);
    return 0;
}
