// LeetCode #2461: Maximum Sum of Distinct Subarrays With Length K -- the
// bench, the ★ arm in C: a sliding window of `k` with a count of each
// value in it and the window's sum. C has no hash map, so the counts
// are an open-addressing table of 2^12 slots keyed by the value, with
// tombstones for removed keys, cleared for every answer.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define CAP (1 << 12)
#define EMPTY 0
#define GONE -1

static int64_t keys[CAP], counts[CAP];
static int64_t size;

static void clear(void) {
    for (int i = 0; i < CAP; i++) keys[i] = EMPTY;
    size = 0;
}

static uint64_t slot_of(int64_t key) {
    return ((uint64_t)key * 0x9E3779B97F4A7C15ULL) >> 52;
}

static void add(int64_t key) {
    uint64_t h = slot_of(key), free = CAP;
    while (keys[h] != EMPTY) {
        if (keys[h] == key) {
            counts[h]++;
            return;
        }
        if (keys[h] == GONE && free == CAP) free = h;
        h = (h + 1) & (CAP - 1);
    }
    if (free == CAP) free = h;
    keys[free] = key;
    counts[free] = 1;
    size++;
}

static void drop(int64_t key) {
    uint64_t h = slot_of(key);
    while (keys[h] != key) h = (h + 1) & (CAP - 1);
    if (--counts[h] == 0) {
        keys[h] = GONE;
        size--;
    }
}

static int64_t maximum_subarray_sum(const int64_t *nums, int64_t n, int64_t k) {
    clear();
    int64_t sum = 0, best = 0;
    for (int64_t i = 0; i < n; i++) {
        add(nums[i]);
        sum += nums[i];
        if (i >= k) {
            drop(nums[i - k]);
            sum -= nums[i - k];
        }
        if (i + 1 >= k && size == k && sum > best) best = sum;
    }
    return best;
}

static int64_t seed = 2461;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

#define ARRAYS 10
#define N 100000

int main(void) {
    // 10 arrays of 10^5 values from 1 to 2000 built once; then 28
    // passes, each setting one value of every array from the checksum so
    // far, then answering every array with k = 5 + 7 p % 40, folding the
    // answer plus the pass into the checksum
    int64_t *arrays = malloc(sizeof(int64_t) * ARRAYS * N);
    for (int64_t i = 0; i < ARRAYS * N; i++) arrays[i] = 1 + next_random() % 2000;
    int64_t check = 0;
    for (int64_t p = 0; p < 28; p++) {
        int64_t k = 5 + 7 * p % 40;
        for (int64_t a = 0; a < ARRAYS; a++) {
            int64_t *row = arrays + a * N;
            row[(check + a) % N] = 1 + check % 2000;
            check = (check * 31 + maximum_subarray_sum(row, N, k) + p) % 1000000007;
        }
    }
    free(arrays);
    printf("28 passes over 10 arrays of 10^5: checksum %lld\n", (long long)check);
    return 0;
}
