// LeetCode #1546: Maximum Number of Non-Overlapping Subarrays With Sum Equals
// Target -- bench: the ★ arm (greedy, a set of prefix sums cleared at each
// cut) over 100 arrays of 1 to 100000 values in -10..10, each with a target
// in -20..20, built once, each asked 5 times. C mirror of subarrays.kara:
// the set is an open-addressing hash table that doubles when half full and
// is cleared over its whole capacity, as a library hash set's clear is.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *keys;
    bool *used;
    int64_t cap, len;
} Set;

static uint64_t hash(int64_t x) {
    uint64_t z = (uint64_t)x + 0x9e3779b97f4a7c15ULL;
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
    z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return z ^ (z >> 31);
}

static void set_init(Set *s) {
    s->cap = 16;
    s->len = 0;
    s->keys = malloc(s->cap * sizeof(int64_t));
    s->used = calloc(s->cap, sizeof(bool));
}

static bool set_contains(const Set *s, int64_t x) {
    uint64_t i = hash(x) & (s->cap - 1);
    while (s->used[i]) {
        if (s->keys[i] == x) return true;
        i = (i + 1) & (s->cap - 1);
    }
    return false;
}

static void set_insert(Set *s, int64_t x);

static void set_grow(Set *s) {
    int64_t *keys = s->keys;
    bool *used = s->used;
    int64_t cap = s->cap;
    s->cap *= 2;
    s->len = 0;
    s->keys = malloc(s->cap * sizeof(int64_t));
    s->used = calloc(s->cap, sizeof(bool));
    for (int64_t i = 0; i < cap; i++) {
        if (used[i]) set_insert(s, keys[i]);
    }
    free(keys);
    free(used);
}

static void set_insert(Set *s, int64_t x) {
    if (2 * (s->len + 1) > s->cap) set_grow(s);
    uint64_t i = hash(x) & (s->cap - 1);
    while (s->used[i]) {
        if (s->keys[i] == x) return;
        i = (i + 1) & (s->cap - 1);
    }
    s->used[i] = true;
    s->keys[i] = x;
    s->len += 1;
}

static void set_clear(Set *s) {
    memset(s->used, 0, s->cap * sizeof(bool));
    s->len = 0;
}

static int64_t max_non_overlapping(const int64_t *nums, int64_t n, int64_t target) {
    Set seen;
    set_init(&seen);
    set_insert(&seen, 0);
    int64_t sum = 0, count = 0;
    for (int64_t i = 0; i < n; i++) {
        sum += nums[i];
        if (set_contains(&seen, sum - target)) {
            count += 1;
            set_clear(&seen);
            set_insert(&seen, 0);
            sum = 0;
        } else {
            set_insert(&seen, sum);
        }
    }
    free(seen.keys);
    free(seen.used);
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    int64_t seed = 1546;
    int64_t *arrays[100];
    int64_t lens[100], targets[100];
    for (int k = 0; k < 100; k++) {
        int64_t a = next_random(&seed);
        int64_t n = (a * 32768 + next_random(&seed)) % 100000 + 1;
        int64_t *nums = malloc(n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) nums[i] = next_random(&seed) % 21 - 10;
        arrays[k] = nums;
        lens[k] = n;
        targets[k] = next_random(&seed) % 41 - 20;
    }
    int64_t check = 0, total = 0;
    for (int p = 0; p < 5; p++) {
        for (int k = 0; k < 100; k++) {
            int64_t answer = max_non_overlapping(arrays[k], lens[k], targets[k]);
            total += answer;
            check = mix(check, answer);
        }
    }
    for (int k = 0; k < 100; k++) free(arrays[k]);
    printf("5 passes over 100 arrays of up to 100000 values: %lld subarrays, checksum %lld\n", (long long)total,
           (long long)check);
    return 0;
}
