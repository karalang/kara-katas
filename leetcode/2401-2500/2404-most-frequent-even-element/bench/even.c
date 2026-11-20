// LeetCode #2404: Most Frequent Even Element -- the bench, the ★ arm in
// C: an open-addressing table of counts of the even values, then every
// slot read for the most frequent and the smallest among equal counts.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 4096

static int64_t seed = 2404;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t most_frequent_even(const int64_t *nums, int64_t n) {
    static int64_t keys[SLOTS], counts[SLOTS];
    memset(counts, 0, sizeof counts);
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        if (x % 2 != 0) continue;
        uint64_t h = ((uint64_t)x * 0x9E3779B97F4A7C15ULL) >> 52;
        while (counts[h] != 0 && keys[h] != x) h = (h + 1) & (SLOTS - 1);
        keys[h] = x;
        counts[h]++;
    }
    int64_t best = -1, most = 0;
    for (int h = 0; h < SLOTS; h++) {
        if (counts[h] == 0) continue;
        if (counts[h] > most || (counts[h] == most && keys[h] < best)) {
            best = keys[h];
            most = counts[h];
        }
    }
    return best;
}

int main(void) {
    static int64_t arrays[200][2000];
    for (int i = 0; i < 200; i++)
        for (int j = 0; j < 2000; j++) arrays[i][j] = next_random() % (1 + 50 * i);
    int64_t check = 0;
    for (int64_t p = 0; p < 100; p++)
        for (int i = 0; i < 200; i++) check = (check * 31 + most_frequent_even(arrays[i], 2000) + 1 + p) % 1000000007;
    printf("100 passes over 200 arrays of 2000 values: checksum %lld\n", (long long)check);
    return 0;
}
