// LeetCode #2364: Count Number of Bad Pairs -- the bench, the ★ arm in C:
// each place's key nums[j] - j counted in a hash map as the places go by,
// the places before j with the same key its good pairs, and the bad pairs
// all n (n - 1) / 2 less the good ones. C has no hash map, so this one is
// open addressing with linear probing over a table of 2^18 slots, the key
// mixed by splitmix64's finalizer.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS (1 << 18)

static uint64_t mix(uint64_t x) {
    x ^= x >> 30;
    x *= 0xbf58476d1ce4e5b9ULL;
    x ^= x >> 27;
    x *= 0x94d049bb133111ebULL;
    x ^= x >> 31;
    return x;
}

static int64_t count_bad_pairs(const int64_t *nums, int64_t n) {
    int64_t *keys = malloc(SLOTS * sizeof(int64_t));
    int64_t *counts = malloc(SLOTS * sizeof(int64_t));
    memset(counts, 0, SLOTS * sizeof(int64_t));
    int64_t good = 0;
    for (int64_t j = 0; j < n; j++) {
        int64_t key = nums[j] - j;
        uint64_t s = mix((uint64_t)key) & (SLOTS - 1);
        while (counts[s] != 0 && keys[s] != key) {
            s = (s + 1) & (SLOTS - 1);
        }
        keys[s] = key;
        good += counts[s];
        counts[s]++;
    }
    free(keys);
    free(counts);
    return n * (n - 1) / 2 - good;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t wide_random(int64_t *seed) {
    int64_t hi = next_random(seed);
    return hi * 32768 + next_random(seed);
}

int main(void) {
    // array a: 10^5 values, each the place plus one of 4^a offsets (at
    // most 10^5) below 999 * 10^6, so the keys run from one to tens of
    // thousands
    const int64_t n = 100000;
    int64_t seed = 2364;
    int64_t *arrays[10];
    int64_t *offsets = malloc(100000 * sizeof(int64_t));
    for (int64_t a = 0; a < 10; a++) {
        int64_t kinds = (int64_t)1 << (2 * a);
        if (kinds > 100000) {
            kinds = 100000;
        }
        for (int64_t k = 0; k < kinds; k++) {
            offsets[k] = wide_random(&seed) % 999000000;
        }
        arrays[a] = malloc(n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            arrays[a][i] = 1 + i + offsets[wide_random(&seed) % kinds];
        }
    }
    free(offsets);
    int64_t check = 0;
    for (int64_t p = 0; p < 20; p++) {
        for (int a = 0; a < 10; a++) {
            check = (check * 31 + count_bad_pairs(arrays[a], n) % 1000000007 + p) % 1000000007;
        }
    }
    printf("20 passes over 10 arrays of 10^5 values: checksum %lld\n", (long long)check);
    for (int a = 0; a < 10; a++) {
        free(arrays[a]);
    }
    return 0;
}
