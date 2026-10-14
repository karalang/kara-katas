// Benchmark for #573: C mirror of the ★ arm (one pass with the best
// first nut); see min_distance.kara. Each nut is its own `malloc`'d pair,
// as the Kāra arm takes a `Vec` of two for each.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t abs64(int64_t x) { return x < 0 ? -x : x; }

static int64_t distance(const int64_t *a, const int64_t *b) {
    return abs64(a[0] - b[0]) + abs64(a[1] - b[1]);
}

static int64_t min_distance(int64_t height, int64_t width, const int64_t *tree,
                            const int64_t *squirrel, int64_t **nuts, int64_t n) {
    (void)height;
    (void)width;
    int64_t total = 0;
    int64_t best_saving = INT64_MIN;
    for (int64_t i = 0; i < n; i++) {
        int64_t to_tree = distance(nuts[i], tree);
        total += 2 * to_tree;
        int64_t saving = to_tree - distance(nuts[i], squirrel);
        if (saving > best_saving) {
            best_saving = saving;
        }
    }
    return total - best_saving;
}

// ---- benchmark --------------------------------------------------------------

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t *cell(int64_t *seed) {
    int64_t *c = malloc(2 * sizeof(int64_t));
    c[0] = next_random(seed) % 100;
    c[1] = next_random(seed) % 100;
    return c;
}

int main(void) {
    int64_t count = 20;
    int64_t rounds = 2000;
    int64_t seed = 573;
    int64_t *trees[20];
    int64_t *squirrels[20];
    int64_t **nut_sets[20];
    for (int64_t g = 0; g < count; g++) {
        trees[g] = cell(&seed);
        squirrels[g] = cell(&seed);
        nut_sets[g] = malloc(5000 * sizeof(int64_t *));
        for (int64_t i = 0; i < 5000; i++) {
            nut_sets[g][i] = cell(&seed);
        }
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int64_t g = 0; g < count; g++) {
            int64_t p = (round * 7 + g) % count;
            int64_t got = min_distance(100, 100, trees[p], squirrels[p], nut_sets[p], 5000);
            total += got;
            checksum = (checksum * 31 + got) % 1000000007;
        }
    }
    printf("%lld cases of 5000 nuts, %lld rounds: %lld steps, checksum %lld\n", (long long)count,
           (long long)rounds, (long long)total, (long long)checksum);
    for (int64_t g = 0; g < count; g++) {
        for (int64_t i = 0; i < 5000; i++) {
            free(nut_sets[g][i]);
        }
        free(nut_sets[g]);
        free(trees[g]);
        free(squirrels[g]);
    }
    return 0;
}
