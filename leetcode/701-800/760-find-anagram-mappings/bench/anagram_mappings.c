// LeetCode 760 — Find Anagram Mappings: benchmark, the ★ arm in C.
// An open-addressing table maps each value to its positions in nums2, in
// order, and to how many of them have been used.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t key;
    int used;      // positions handed out so far
    int count;     // positions listed
    int cap;
    int64_t *positions;
    int full;
} Slot;

static Slot *find(Slot *table, int cap, int64_t key) {
    size_t i = (size_t)(((uint64_t)key * 0x9E3779B97F4A7C15ull) >> 40) & (size_t)(cap - 1);
    while (table[i].full && table[i].key != key) i = (i + 1) & (size_t)(cap - 1);
    return &table[i];
}

static void anagram_mappings(const int64_t *nums1, const int64_t *nums2, int n, int64_t *mapping) {
    int cap = 1;
    while (cap < 2 * n) cap *= 2;
    Slot *table = calloc((size_t)cap, sizeof(Slot));
    for (int j = 0; j < n; j++) {
        Slot *s = find(table, cap, nums2[j]);
        if (!s->full) {
            s->full = 1;
            s->key = nums2[j];
        }
        if (s->count == s->cap) {
            s->cap = s->cap ? s->cap * 2 : 1;
            s->positions = realloc(s->positions, (size_t)s->cap * sizeof(int64_t));
        }
        s->positions[s->count++] = j;
    }
    for (int i = 0; i < n; i++) {
        Slot *s = find(table, cap, nums1[i]);
        mapping[i] = s->positions[s->used++];
    }
    for (int i = 0; i < cap; i++) free(table[i].positions);
    free(table);
}

static int64_t seed = 760;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t rounds = 100000, fixed = 0, check = 0;
    int64_t nums1[100], nums2[100], mapping[100];
    for (int64_t r = 0; r < rounds; r++) {
        for (int i = 0; i < 100; i++) nums1[i] = next_random() % 50;
        memcpy(nums2, nums1, sizeof nums1);
        for (int i = 0; i < 100; i++) {
            int j = i + (int)(next_random() % (100 - i));
            int64_t t = nums2[i];
            nums2[i] = nums2[j];
            nums2[j] = t;
        }
        anagram_mappings(nums1, nums2, 100, mapping);
        for (int i = 0; i < 100; i++) {
            if (mapping[i] == i) fixed++;
            check = (check * 31 + mapping[i]) % 1000000007;
        }
    }
    printf("%lld pairs of 100 values: %lld mapped to their own index, checksum %lld\n", (long long)rounds,
           (long long)fixed, (long long)check);
    return 0;
}
