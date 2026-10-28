// Benchmark: LeetCode #1007 Minimum Domino Rotations For Equal Row -- the
// ★ arm, two candidates, on rows of 20000 dominoes, LeetCode's longest.
// Mirrors min_rotations.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t rotations(const int64_t *tops, const int64_t *bottoms, int64_t n, int64_t v) {
    int64_t to_top = 0, to_bottom = 0;
    for (int64_t i = 0; i < n; i++) {
        if (tops[i] != v && bottoms[i] != v) return -1;
        if (tops[i] != v) {
            to_top++;
        } else if (bottoms[i] != v) {
            to_bottom++;
        }
    }
    return to_top < to_bottom ? to_top : to_bottom;
}

static int64_t min_domino_rotations(const int64_t *tops, const int64_t *bottoms, int64_t n) {
    int64_t a = rotations(tops, bottoms, n, tops[0]);
    int64_t b = rotations(tops, bottoms, n, bottoms[0]);
    if (a == -1) return b;
    if (b == -1) return a;
    return a < b ? a : b;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t rounds = 400;
    int64_t n = 20000;
    int64_t seed = 1007;
    int64_t *all_tops[20], *all_bottoms[20];
    for (int64_t t = 0; t < 20; t++) {
        int64_t target = t % 6 + 1;
        all_tops[t] = malloc(n * sizeof(int64_t));
        all_bottoms[t] = malloc(n * sizeof(int64_t));
        for (int64_t j = 0; j < n; j++) {
            int64_t top = 1 + next_random(&seed) % 6;
            int64_t bottom = 1 + next_random(&seed) % 6;
            if (t % 2 == 0 || next_random(&seed) % 2000 != 0) {
                if (next_random(&seed) % 2 == 0) {
                    top = target;
                } else {
                    bottom = target;
                }
            }
            all_tops[t][j] = top;
            all_bottoms[t][j] = bottom;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < 20; i++) {
            int64_t t = (r + i) % 20;
            int64_t got = min_domino_rotations(all_tops[t], all_bottoms[t], n);
            total += got;
            check = (check * 31 + got + 2) % 1000000007;
        }
    }
    printf("%lld rounds over 20 rows of %lld dominoes: answers sum to %lld, checksum %lld\n",
           (long long)rounds, (long long)n, (long long)total, (long long)check);
    for (int64_t t = 0; t < 20; t++) {
        free(all_tops[t]);
        free(all_bottoms[t]);
    }
    return 0;
}
