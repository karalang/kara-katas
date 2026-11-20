// LeetCode #2367: Number of Arithmetic Triplets -- the bench, the ★ arm in
// C: a hash set of the values, and each value x the start of a triplet
// when the set holds x + diff and x + 2 diff. C has no hash set, so this
// one is open addressing with linear probing over a table of 2^10 slots,
// the key mixed by splitmix64's finalizer, built afresh in each call.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define SLOTS (1 << 10)

static uint64_t mix(uint64_t x) {
    x ^= x >> 30;
    x *= 0xbf58476d1ce4e5b9ULL;
    x ^= x >> 27;
    x *= 0x94d049bb133111ebULL;
    x ^= x >> 31;
    return x;
}

static void insert(int64_t *keys, bool *used, int64_t key) {
    uint64_t s = mix((uint64_t)key) & (SLOTS - 1);
    while (used[s] && keys[s] != key) {
        s = (s + 1) & (SLOTS - 1);
    }
    used[s] = true;
    keys[s] = key;
}

static bool contains(const int64_t *keys, const bool *used, int64_t key) {
    uint64_t s = mix((uint64_t)key) & (SLOTS - 1);
    while (used[s]) {
        if (keys[s] == key) {
            return true;
        }
        s = (s + 1) & (SLOTS - 1);
    }
    return false;
}

static int64_t arithmetic_triplets(const int64_t *nums, int64_t n, int64_t diff) {
    int64_t *keys = malloc(SLOTS * sizeof(int64_t));
    bool *used = calloc(SLOTS, sizeof(bool));
    for (int64_t i = 0; i < n; i++) {
        insert(keys, used, nums[i]);
    }
    int64_t count = 0;
    for (int64_t i = 0; i < n; i++) {
        if (contains(keys, used, nums[i] + diff) && contains(keys, used, nums[i] + 2 * diff)) {
            count++;
        }
    }
    free(keys);
    free(used);
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // set s: each value from 0 to 200 kept with a chance of 1 + s % 8 in 8,
    // and at least the three values 0, 1 and 2
    int64_t seed = 2367;
    int64_t *sets[1000];
    int64_t sizes[1000];
    for (int64_t s = 0; s < 1000; s++) {
        sets[s] = malloc(201 * sizeof(int64_t));
        sizes[s] = 0;
        for (int64_t v = 0; v < 201; v++) {
            if (v < 3 || next_random(&seed) % 8 <= s % 8) {
                sets[s][sizes[s]++] = v;
            }
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 50; p++) {
        for (int64_t s = 0; s < 1000; s++) {
            int64_t diff = 1 + (s + p) % 50;
            check = (check * 31 + arithmetic_triplets(sets[s], sizes[s], diff) + p) % 1000000007;
        }
    }
    printf("50 passes over 1000 sets of up to 201 values: checksum %lld\n", (long long)check);
    for (int s = 0; s < 1000; s++) {
        free(sets[s]);
    }
    return 0;
}
