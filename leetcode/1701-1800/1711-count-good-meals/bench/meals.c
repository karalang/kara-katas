// LeetCode #1711: Count Good Meals -- the C mirror of the bench
// (meals.kara): one pass, each dish paired with the earlier dishes that
// make each of the 22 powers with it, counted in a hash map, on 10 random
// lists of 100000 dishes, each answered 3 times.
//
// C has no map: this one is open addressing with linear probing, keys
// hashed by a multiply, a table of 2^18 slots made for each answer.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define SLOTS (1 << 18)

typedef struct {
    int32_t key;
    int used;
    int64_t count;
} Slot;

static size_t slot_of(const Slot *table, int32_t key) {
    size_t i = (size_t)(((uint32_t)key * 2654435769u) >> 14);
    while (table[i].used && table[i].key != key) {
        i = (i + 1) & (SLOTS - 1);
    }
    return i;
}

static int count_pairs(const int32_t *deliciousness, int n) {
    Slot *seen = calloc(SLOTS, sizeof(Slot));
    int64_t pairs = 0;
    for (int i = 0; i < n; i++) {
        int32_t d = deliciousness[i];
        for (int b = 0; b < 22; b++) {
            size_t s = slot_of(seen, (1 << b) - d);
            if (seen[s].used) {
                pairs += seen[s].count;
            }
        }
        size_t s = slot_of(seen, d);
        seen[s].used = 1;
        seen[s].key = d;
        seen[s].count += 1;
    }
    free(seen);
    return (int)(pairs % 1000000007);
}

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int count = 10;
    const long long rounds = 3;
    const int n = 100000;
    const long long top = 1 << 20;
    long long seed = 1711;
    int32_t *lists = malloc(sizeof(int32_t) * count * n);
    for (int p = 0; p < count; p++) {
        for (int i = 0; i < n; i++) {
            long long a = next_random(&seed);
            lists[p * n + i] = (int32_t)((a * 32768 + next_random(&seed)) % (top + 1));
        }
    }
    long long sum = 0;
    long long check = 0;
    for (long long r = 0; r < rounds; r++) {
        for (int p = 0; p < count; p++) {
            long long answer = count_pairs(lists + p * n, n);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d lists of %d dishes, %lld rounds: answers sum to %lld, checksum %lld\n", count, n, rounds, sum, check);
    free(lists);
    return 0;
}
