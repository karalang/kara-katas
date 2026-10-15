// LeetCode #646: Maximum Length of Pair Chain -- C mirror of the Kāra
// bench.
//
// The ★ arm's greedy over the same inputs and rounds: the pairs, a flat
// array of (left, right), copied and sorted by right end, then every
// pair kept that starts after the last one kept ended.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t left;
    int64_t right;
} Pair;

static int by_right(const void *a, const void *b) {
    int64_t x = ((const Pair *)a)->right, y = ((const Pair *)b)->right;
    return (x > y) - (x < y);
}

static int64_t find_longest_chain(const Pair *pairs, int64_t n) {
    Pair *order = malloc(n * sizeof(Pair));
    memcpy(order, pairs, n * sizeof(Pair));
    qsort(order, n, sizeof(Pair), by_right);
    int64_t count = 0, end = 0;
    for (int64_t i = 0; i < n; i++) {
        if (count == 0 || order[i].left > end) {
            count++;
            end = order[i].right;
        }
    }
    free(order);
    return count;
}

static int64_t seed = 646;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    enum { INPUTS = 20, ROUNDS = 200, COUNT = 10000 };
    Pair *all[INPUTS];
    for (int i = 0; i < INPUTS; i++) {
        int64_t longest = 10 + next_random() % 991;
        all[i] = malloc(COUNT * sizeof(Pair));
        for (int j = 0; j < COUNT; j++) {
            int64_t left = next_random() % 30000;
            int64_t right = left + 1 + next_random() % longest;
            all[i][j].left = left;
            all[i][j].right = right;
        }
    }
    int64_t sum = 0, checksum = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        int64_t c = find_longest_chain(all[(r * 7) % INPUTS], COUNT);
        sum += c;
        checksum = (checksum * 31 + c) % 1000000007;
    }
    printf("%d inputs, %d rounds: total %lld, checksum %lld\n", INPUTS, ROUNDS, (long long)sum, (long long)checksum);
    for (int i = 0; i < INPUTS; i++) free(all[i]);
    return 0;
}
