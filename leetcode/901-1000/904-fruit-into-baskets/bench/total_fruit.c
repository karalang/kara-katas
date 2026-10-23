// LeetCode #904: Fruit Into Baskets -- bench program, C.
//
// The last two types and the last run, over one row of 1,000,000 trees
// built once, of 3 types in runs of 1 to 50 trees. Each round finds the
// most fruit, folds it into a checksum and changes one tree's type.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t total_fruit(const int64_t *fruits, int64_t n) {
    int64_t last = -1, before = -1, run = 0, current = 0, best = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t f = fruits[i];
        if (f == last || f == before) {
            current += 1;
        } else {
            current = run + 1;
        }
        if (f == last) {
            run += 1;
        } else {
            run = 1;
            before = last;
            last = f;
        }
        if (current > best) best = current;
    }
    return best;
}

static int64_t seed = 904;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t trees = 1000000;
    int64_t rounds = 240;
    int64_t *fruits = malloc(sizeof(int64_t) * trees);
    int64_t len = 0;
    while (len < trees) {
        int64_t f = next_random() % 3;
        int64_t r = 1 + next_random() % 50;
        for (int64_t k = 0; k < r; k++) {
            if (len < trees) fruits[len++] = f;
        }
    }
    int64_t check = 0, total = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t got = total_fruit(fruits, trees);
        total += got;
        check = (check * 31 + got) % 1000000007;
        fruits[round * 7919 % trees] = next_random() % 3;
    }
    printf("%lld rounds over %lld trees: answers summing to %lld, checksum %lld\n", (long long)rounds,
           (long long)trees, (long long)total, (long long)check);
    free(fruits);
    return 0;
}
