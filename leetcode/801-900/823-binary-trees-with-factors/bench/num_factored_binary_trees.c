// Benchmark for #823: Binary Trees With Factors -- the ★ arm (counts in a map).
//
// Mirrors num_factored_binary_trees.kara: sort a copy of the values, so
// that both factors of a value come before it, and count each value's
// trees from its factors' counts, looked up by value in a map. C has no
// hash map, so this one is open addressing over the values, which are
// never 0, with a multiplicative hash.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t key;
    int64_t value;
} Slot;

static uint64_t slot_of(int64_t x, int64_t cap) {
    return ((uint64_t)x * 11400714819323198485ULL) >> 32 & (uint64_t)(cap - 1);
}

static Slot *find(Slot *table, int64_t cap, int64_t x) {
    uint64_t i = slot_of(x, cap);
    while (table[i].key != 0 && table[i].key != x) i = (i + 1) & (uint64_t)(cap - 1);
    return &table[i];
}

static int compare(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t num_factored_binary_trees(const int64_t *arr, int64_t n) {
    const int64_t modulus = 1000000007;
    int64_t *values = malloc((size_t)n * sizeof(int64_t));
    memcpy(values, arr, (size_t)n * sizeof(int64_t));
    qsort(values, (size_t)n, sizeof(int64_t), compare);
    int64_t cap = 16;
    while (cap < 2 * n) cap *= 2;
    Slot *trees = calloc((size_t)cap, sizeof(Slot));
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = values[i];
        int64_t count = 1;
        for (int64_t j = 0; j < i; j++) {
            int64_t left = values[j];
            if (x % left == 0) {
                Slot *right = find(trees, cap, x / left);
                if (right->key != 0) count = (count + find(trees, cap, left)->value * right->value) % modulus;
            }
        }
        Slot *s = find(trees, cap, x);
        s->key = x;
        s->value = count;
        total = (total + count) % modulus;
    }
    free(values);
    free(trees);
    return total;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const int64_t limit = 1000000000;
    int64_t *smooth = malloc(8192 * sizeof(int64_t));
    int64_t ns = 0;
    for (int64_t p2 = 1; p2 <= limit; p2 *= 2)
        for (int64_t p3 = p2; p3 <= limit; p3 *= 3)
            for (int64_t p5 = p3; p5 <= limit; p5 *= 5)
                for (int64_t p7 = p5; p7 <= limit; p7 *= 7)
                    if (p7 > 1) smooth[ns++] = p7;
    qsort(smooth, (size_t)ns, sizeof(int64_t), compare);
    int64_t count = 64;
    int64_t rounds = 1000;
    int64_t seed = 823;
    int64_t *sets[64];
    char *taken = malloc((size_t)ns);
    for (int64_t g = 0; g < count; g++) {
        memset(taken, 0, (size_t)ns);
        sets[g] = malloc(1000 * sizeof(int64_t));
        int64_t len = 0;
        while (len < 1000) {
            int64_t k = next_random(&seed) % ns;
            if (!taken[k]) {
                taken[k] = 1;
                sets[g][len++] = smooth[k];
            }
        }
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t answer = num_factored_binary_trees(sets[round % count], 1000);
        total += answer;
        checksum = (checksum * 131 + answer) % 1000000007;
    }
    printf("%lld values, %lld rounds of %lld sets: total %lld, checksum %lld\n", (long long)ns,
           (long long)rounds, (long long)count, (long long)total, (long long)checksum);
    return 0;
}
