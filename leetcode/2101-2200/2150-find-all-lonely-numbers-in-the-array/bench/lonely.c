// LeetCode #2150: Find All Lonely Numbers in the Array -- the benchmark's
// C mirror of lonely.kara; the map of counts is an open-addressing hash
// table, C having none of its own.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000
#define SLOTS 262144 /* a power of two, over twice N */

static int64_t keys[SLOTS];
static char used[SLOTS];
static int64_t counts[SLOTS];

static uint64_t slot_of(int64_t key) {
    uint64_t x = (uint64_t)key * 0x9E3779B97F4A7C15ull;
    return (x ^ (x >> 29)) & (SLOTS - 1);
}

static uint64_t find(int64_t key) {
    uint64_t s = slot_of(key);
    while (used[s] && keys[s] != key) s = (s + 1) & (SLOTS - 1);
    return s;
}

static int contains(int64_t key) {
    return used[find(key)];
}

static int64_t *find_lonely(const int64_t *nums, int64_t n, int64_t *len) {
    for (int i = 0; i < SLOTS; i++) used[i] = 0;
    for (int64_t i = 0; i < n; i++) {
        uint64_t s = find(nums[i]);
        if (!used[s]) {
            used[s] = 1;
            keys[s] = nums[i];
            counts[s] = 0;
        }
        counts[s]++;
    }
    int64_t *out = malloc(sizeof(int64_t) * (size_t)n);
    int64_t k = 0;
    for (int i = 0; i < SLOTS; i++) {
        if (used[i] && counts[i] == 1 && !contains(keys[i] - 1) && !contains(keys[i] + 1)) {
            out[k++] = keys[i];
        }
    }
    *len = k;
    return out;
}

static int64_t seed = 2150;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    int64_t *lists[4];
    for (int l = 0; l < 4; l++) {
        lists[l] = malloc(sizeof(int64_t) * N);
        for (int64_t i = 0; i < N; i++) lists[l][i] = wide() % 1000001;
    }
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t round = 0; round < 25; round++) {
        for (int l = 0; l < 4; l++) {
            int64_t at = wide() % N;
            lists[l][at] = wide() % 1000001;
            int64_t len;
            int64_t *out = find_lonely(lists[l], N, &len);
            int64_t sum = 0;
            for (int64_t i = 0; i < len; i++) sum += out[i];
            free(out);
            total += len;
            check = (check * 31 + sum % 1000000007 + len + round) % 1000000007;
        }
    }
    printf("100 searches: %lld lonely in all, checksum %lld\n", (long long)total, (long long)check);
    for (int l = 0; l < 4; l++) free(lists[l]);
    return 0;
}
