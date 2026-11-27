// LeetCode #1814: Count Nice Pairs in an Array -- the bench in C: the ★
// arm over 200 calls on runs of 50000 to 99999 numbers cut from one array
// of 10^5, built once, each run's length drawn from the checksum so far.
// The map is an open-addressing hash table of the differences.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MOD 1000000007

static int64_t rev(int64_t x) {
    int64_t r = 0;
    while (x > 0) {
        r = r * 10 + x % 10;
        x /= 10;
    }
    return r;
}

static uint64_t mix(uint64_t k) {
    k ^= k >> 33;
    k *= 0xff51afd7ed558ccdULL;
    k ^= k >> 33;
    k *= 0xc4ceb9fe1a85ec53ULL;
    k ^= k >> 33;
    return k;
}

static int64_t count_nice_pairs(const int64_t *nums, size_t n) {
    size_t cap = 1;
    while (cap < 2 * n)
        cap <<= 1;
    int64_t *keys = malloc(cap * sizeof(int64_t));
    int64_t *counts = calloc(cap, sizeof(int64_t));
    int64_t pairs = 0;
    for (size_t i = 0; i < n; i++) {
        int64_t d = nums[i] - rev(nums[i]);
        size_t at = mix((uint64_t)d) & (cap - 1);
        while (counts[at] != 0 && keys[at] != d)
            at = (at + 1) & (cap - 1);
        keys[at] = d;
        pairs = (pairs + counts[at]) % MOD;
        counts[at]++;
    }
    free(keys);
    free(counts);
    return pairs;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1814;
    int64_t *base = malloc(100000 * sizeof(int64_t));
    for (int k = 0; k < 100000; k++) {
        if (k % 2 == 0)
            base[k] = next_random(&seed) % 10000;
        else {
            int64_t hi = next_random(&seed);
            base[k] = (hi * 32768 + next_random(&seed)) % 1000000001;
        }
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 200; call++) {
        size_t n = (size_t)(50000 + (check + call) % 50000);
        check = (check * 31 + count_nice_pairs(base, n)) % MOD;
    }
    printf("200 calls: checksum %lld\n", (long long)check);
    free(base);
    return 0;
}
