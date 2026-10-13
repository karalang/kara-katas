// Benchmark for #532: C mirror of the ★ arm (count each number); see
// find_pairs.kara. C has no map, so each call builds a fresh
// open-addressing table (linear probing, a multiplicative hash) sized
// to twice the numbers, as the ★ arm builds a fresh `Map`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t key, count;
    int used;
} Slot;

typedef struct {
    Slot *slots;
    uint64_t mask;
} Table;

static uint64_t hash(int64_t key) { return (uint64_t)key * 0x9E3779B97F4A7C15ULL; }

static Slot *find(const Table *t, int64_t key) {
    uint64_t i = (hash(key) >> 32) & t->mask;
    while (t->slots[i].used && t->slots[i].key != key) i = (i + 1) & t->mask;
    return &t->slots[i];
}

static int64_t find_pairs(const int64_t *nums, int64_t n, int64_t k) {
    uint64_t size = 1;
    while (size < 2 * (uint64_t)n) size *= 2;
    Table t = {calloc(size, sizeof(Slot)), size - 1};
    for (int64_t i = 0; i < n; i++) {
        Slot *s = find(&t, nums[i]);
        if (!s->used) {
            s->used = 1;
            s->key = nums[i];
        }
        s->count++;
    }
    int64_t pairs = 0;
    for (uint64_t i = 0; i < size; i++) {
        if (!t.slots[i].used) continue;
        if (k == 0) {
            if (t.slots[i].count >= 2) pairs++;
        } else if (find(&t, t.slots[i].key + k)->used) {
            pairs++;
        }
    }
    free(t.slots);
    return pairs;
}

int main(void) {
    // 20 arrays of 10,000 numbers made once, the a-th drawn from
    // -1,000(a + 1) to 1,000(a + 1); then each array is answered for 200
    // values of k from 0 to 19.
    int64_t seed = 532;
    int64_t *arrays[20];
    for (int a = 0; a < 20; a++) {
        int64_t half = 1000 * (a + 1);
        arrays[a] = malloc(10000 * sizeof(int64_t));
        for (int i = 0; i < 10000; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            arrays[a][i] = seed / 65536 % (2 * half + 1) - half;
        }
    }
    int64_t total = 0, checksum = 0;
    for (int round = 0; round < 200; round++) {
        for (int a = 0; a < 20; a++) {
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            int64_t answer = find_pairs(arrays[a], 10000, seed / 65536 % 20);
            total += answer;
            checksum = (checksum * 31 + answer) % 1000000007;
        }
    }
    printf("20 arrays of 10000, 200 values of k each: total %lld, checksum %lld\n", (long long)total,
           (long long)checksum);
    for (int a = 0; a < 20; a++) free(arrays[a]);
    return 0;
}
