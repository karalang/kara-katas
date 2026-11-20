// LeetCode #2354: Number of Excellent Pairs -- the bench, the ★ arm in C:
// the distinct values tallied by their count of set bits, then every two
// tallies whose bits reach k multiplied. C has no set, so the distinct
// values are found in a table of 2^18 slots by open addressing, cleared
// for each call.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS (1 << 18)

static int64_t table[SLOTS];

static int64_t count_excellent_pairs(const int64_t *nums, int n, int64_t k) {
    memset(table, 0, sizeof table);
    int64_t by_bits[31] = {0};
    for (int i = 0; i < n; i++) {
        int64_t x = nums[i];
        size_t s = ((uint64_t)x * 0x9E3779B97F4A7C15ULL) >> 46;
        while (table[s] != 0 && table[s] != x) {
            s = (s + 1) & (SLOTS - 1);
        }
        if (table[s] == 0) {
            table[s] = x;
            by_bits[__builtin_popcountll((uint64_t)x)]++;
        }
    }
    int64_t total = 0;
    for (int a = 0; a < 31; a++) {
        for (int b = 0; b < 31; b++) {
            if (a + b >= k) {
                total += by_bits[a] * by_bits[b];
            }
        }
    }
    return total;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // array a holds 10^5 values from 1 to 10^9, from 1 to 10^(4 + a / 2)
    // distinct; pass p asks for k = 1 + (7 p + a) mod 60
    int64_t seed = 2354;
    int64_t *arrays = malloc(10 * 100000 * sizeof(int64_t));
    int64_t spread = 10000;
    for (int a = 0; a < 10; a++) {
        for (int i = 0; i < 100000; i++) {
            int64_t high = next_random(&seed);
            arrays[a * 100000 + i] = 1 + (high * 32768 + next_random(&seed)) % spread * 99991 % 1000000000;
        }
        if (a % 2 == 1) {
            spread *= 10;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 20; p++) {
        for (int64_t a = 0; a < 10; a++) {
            int64_t k = 1 + (7 * p + a) % 60;
            check = (check * 31 + count_excellent_pairs(arrays + a * 100000, 100000, k) + p) % 1000000007;
        }
    }
    printf("20 passes over 10 arrays of 10^5 values: checksum %lld\n", (long long)check);
    free(arrays);
    return 0;
}
