// LeetCode #2501: Longest Square Streak in an Array -- C mirror of the
// benchmark (square.kara): the same arrays, passes and checksum; the
// values in an open-addressed hash set, calloc'd on every ask, of
// 2^18 slots probed linearly from a splitmix hash, 0 the empty slot.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define SLOTS (1 << 18)

static int64_t seed = 2501;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t below(int64_t top) {
    int64_t hi = next_random();
    return (hi * 32768 + next_random()) % top;
}

static uint64_t slot_of(int64_t v) {
    uint64_t z = (uint64_t)v + 0x9e3779b97f4a7c15ULL;
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
    z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return (z ^ (z >> 31)) & (SLOTS - 1);
}

// adds v; returns 1 when it was not there yet
static int insert(int64_t *table, int64_t v) {
    uint64_t s = slot_of(v);
    while (table[s] != 0) {
        if (table[s] == v) return 0;
        s = (s + 1) & (SLOTS - 1);
    }
    table[s] = v;
    return 1;
}

static int contains(const int64_t *table, int64_t v) {
    uint64_t s = slot_of(v);
    while (table[s] != 0) {
        if (table[s] == v) return 1;
        s = (s + 1) & (SLOTS - 1);
    }
    return 0;
}

static int64_t isqrt(int64_t v) {
    int64_t r = 0;
    for (int64_t step = 1 << 16; step > 0; step >>= 1) {
        if ((r + step) * (r + step) <= v) r += step;
    }
    return r;
}

static int64_t longest_square_streak(const int64_t *nums, int64_t n, int64_t *distinct) {
    int64_t *table = calloc(SLOTS, sizeof(int64_t));
    int64_t count = 0;
    for (int64_t i = 0; i < n; i++) {
        if (insert(table, nums[i])) distinct[count++] = nums[i];
    }
    int64_t best = 0;
    for (int64_t i = 0; i < count; i++) {
        int64_t v = distinct[i];
        int64_t r = isqrt(v);
        if (r * r == v && contains(table, r)) continue;
        int64_t length = 0;
        for (int64_t x = v; contains(table, x); x = x * x) length++;
        if (length > best) best = length;
    }
    free(table);
    return best >= 2 ? best : -1;
}

static void chained(int64_t *out, int64_t n) {
    for (int64_t i = 0; i < n; i++) {
        if (next_random() % 4 == 0) {
            out[i] = below(99999) + 2;
        } else {
            int64_t v = next_random() % 19 + 2;
            int64_t times = next_random() % 4;
            for (int64_t t = 0; t < times; t++) {
                if (v * v <= 100000) v = v * v;
            }
            out[i] = v;
        }
    }
}

int main(void) {
    const int64_t passes = 32, n = 100000;
    int64_t *arrays[20];
    int64_t *distinct = malloc(n * sizeof(int64_t));
    for (int q = 0; q < 20; q++) {
        arrays[q] = malloc(n * sizeof(int64_t));
        chained(arrays[q], n);
    }
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++) {
        for (int q = 0; q < 20; q++) {
            int64_t at = check % n;
            int64_t was = arrays[q][at];
            arrays[q][at] = (check + p) % 99999 + 2;
            check = (check * 31 + longest_square_streak(arrays[q], n, distinct) + 1 + p) % 1000000007;
            arrays[q][at] = was;
        }
    }
    printf("%lld passes over 20 arrays of 10^5: checksum %lld\n", (long long)passes, (long long)check);
    for (int q = 0; q < 20; q++) free(arrays[q]);
    free(distinct);
    return 0;
}
