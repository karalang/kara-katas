// LeetCode #2845: Count of Interesting Subarrays -- the bench, mirrored
// from interesting.kara: a map from each prefix count mod modulo to how
// often it has come up, here an open-addressed table, read before each
// new prefix is added.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 262144  // a power of two above twice the most prefixes

static int64_t keys[SLOTS], vals[SLOTS];
static unsigned char used[SLOTS];

static long slot(int64_t key) {
    long s = (long)(((uint64_t)key * 0x9E3779B97F4A7C15ull) >> 46);
    while (used[s] && keys[s] != key) s = (s + 1) & (SLOTS - 1);
    return s;
}

static int64_t count_interesting_subarrays(const int64_t *nums, long n, int64_t modulo, int64_t k) {
    memset(used, 0, sizeof used);
    long s = slot(0);
    used[s] = 1;
    keys[s] = 0;
    vals[s] = 1;
    int64_t prefix = 0, count = 0;
    for (long i = 0; i < n; i++) {
        if (nums[i] % modulo == k) prefix = (prefix + 1) % modulo;
        int64_t want = (prefix - k + modulo) % modulo;
        long w = slot(want);
        if (used[w]) count += vals[w];
        long p = slot(prefix);
        if (!used[p]) {
            used[p] = 1;
            keys[p] = prefix;
            vals[p] = 0;
        }
        vals[p]++;
    }
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const long count = 10, n = 100000, rounds = 20;
    int64_t seed = 2845;
    int64_t *nums = malloc(count * n * sizeof(int64_t));
    int64_t mods[10], ks[10];
    for (long c = 0; c < count; c++) {
        for (long i = 0; i < n; i++) {
            int64_t hi = next_random(&seed);
            nums[c * n + i] = (hi * 32768 + next_random(&seed)) % 1000000000 + 1;
        }
        mods[c] = next_random(&seed) % (c % 2 == 0 ? 10 : 100000) + 1;
        ks[c] = next_random(&seed) % mods[c];
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (long c = 0; c < count; c++) {
            int64_t got = count_interesting_subarrays(nums + c * n, n, mods[c], ks[c]);
            total += got;
            check = (check * 31 + got % 1000000007 + r) % 1000000007;
        }
    }
    printf("%ld arrays of %ld, %ld rounds: %lld subarrays, checksum %lld\n", count, n, rounds, (long long)total, (long long)check);
    free(nums);
    return 0;
}
