// LeetCode #2841: Maximum Sum of Almost Unique Subarray -- the bench,
// mirrored from almost.kara: a window of k slid along the array, its
// sum kept and a map from each value in it to its count, here an
// open-addressed table with backward-shift deletion.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 16384  // a power of two above the window's most values

static int64_t keys[SLOTS], vals[SLOTS];
static long used;

static long slot(int64_t key) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ull;
    long s = (long)(h >> 50);
    while (keys[s] != 0 && keys[s] != key) s = (s + 1) & (SLOTS - 1);
    return s;
}

static void add(int64_t key) {
    long s = slot(key);
    if (keys[s] == 0) {
        keys[s] = key;
        vals[s] = 0;
        used++;
    }
    vals[s]++;
}

static void drop_one(int64_t key) {
    long s = slot(key);
    if (--vals[s] > 0) return;
    used--;
    keys[s] = 0;
    long j = s;
    for (;;) {
        j = (j + 1) & (SLOTS - 1);
        if (keys[j] == 0) return;
        long home = (long)(((uint64_t)keys[j] * 0x9E3779B97F4A7C15ull) >> 50);
        // move j back into the hole at s unless its home lies in (s, j]
        if ((s < j) ? (home <= s || home > j) : (home <= s && home > j)) {
            keys[s] = keys[j];
            vals[s] = vals[j];
            keys[j] = 0;
            s = j;
        }
    }
}

static int64_t max_sum(const int64_t *nums, long n, int64_t m, int64_t k) {
    memset(keys, 0, sizeof keys);
    used = 0;
    int64_t sum = 0, best = 0;
    for (long i = 0; i < n; i++) {
        add(nums[i]);
        sum += nums[i];
        if (i >= k) {
            sum -= nums[i - k];
            drop_one(nums[i - k]);
        }
        if (i + 1 >= k && used >= m && sum > best) best = sum;
    }
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const long count = 100, n = 20000, rounds = 20;
    int64_t seed = 2841;
    int64_t *nums = malloc(count * n * sizeof(int64_t));
    int64_t ms[100], ks[100];
    for (long c = 0; c < count; c++) {
        for (long i = 0; i < n; i++) nums[c * n + i] = next_random(&seed) % 10000 + 1;
        ks[c] = next_random(&seed) % 5000 + 1;
        ms[c] = next_random(&seed) % ks[c] + 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (long c = 0; c < count; c++) {
            int64_t best = max_sum(nums + c * n, n, ms[c], ks[c]);
            total += best;
            check = (check * 31 + best + r) % 1000000007;
        }
    }
    printf("%ld arrays of %ld, %ld rounds: sums total %lld, checksum %lld\n", count, n, rounds, (long long)total, (long long)check);
    free(nums);
    return 0;
}
