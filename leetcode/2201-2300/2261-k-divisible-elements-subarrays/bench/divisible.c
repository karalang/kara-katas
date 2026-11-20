// LeetCode #2261: K Divisible Elements Subarrays -- C mirror of the ★
// arm: from every start the subarray grows until more than k of its
// elements are divisible by p, each one put into a set. C has no set of
// arrays, so the set is an open-addressing table: each subarray is
// hashed whole (FNV-1a over its elements), compared element by element
// on a hash match, and stored as its own copy when new, as the ★ arm
// clones `run` into its `Set`. Same workload and checksum as
// divisible.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t seed = 2261;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct { int64_t *items; int32_t len; uint64_t hash; } Entry;

static int64_t count_distinct(const int64_t *nums, int n, int64_t k, int64_t p) {
    int cap = 1;
    while (cap < 2 * n * (n + 1) / 2 + 2) cap <<= 1;
    Entry *table = calloc(cap, sizeof(Entry));
    int64_t count = 0;
    for (int start = 0; start < n; start++) {
        int64_t divisible = 0;
        for (int end = start; end < n; end++) {
            if (nums[end] % p == 0) divisible++;
            if (divisible > k) break;
            const int64_t *run = nums + start;
            int len = end - start + 1;
            uint64_t h = 1469598103934665603ULL;
            for (int i = 0; i < len; i++) h = (h ^ (uint64_t)run[i]) * 1099511628211ULL;
            int slot = (int)(h & (uint64_t)(cap - 1));
            for (;;) {
                Entry *e = &table[slot];
                if (e->len == 0) {
                    e->items = malloc(sizeof(int64_t) * len);
                    memcpy(e->items, run, sizeof(int64_t) * len);
                    e->len = len;
                    e->hash = h;
                    count++;
                    break;
                }
                if (e->hash == h && e->len == len && memcmp(e->items, run, sizeof(int64_t) * len) == 0) break;
                slot = (slot + 1) & (cap - 1);
            }
        }
    }
    for (int i = 0; i < cap; i++) free(table[i].items);
    free(table);
    return count;
}

int main(void) {
    int64_t nums[200];
    int64_t check = 0;
    for (int t = 0; t < 40; t++) {
        for (int i = 0; i < 200; i++) nums[i] = next_random() % 200 + 1;
        int64_t p = next_random() % 8 + 2;
        int64_t k = next_random() % 196 + 5;
        check = (check * 31 + count_distinct(nums, 200, k, p)) % 1000000007;
    }
    printf("40 arrays of 200: checksum %lld\n", (long long)check);
    return 0;
}
