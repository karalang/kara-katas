// Benchmark for #452: mirror of min_arrows.kara (greedy by end) on 10
// random sets of 100,000 balloons over the 32-bit range, built once,
// then each counted 10 times.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t start;
    int64_t end;
} Balloon;

static int by_end(const void *a, const void *b) {
    const Balloon *x = a, *y = b;
    return (x->end > y->end) - (x->end < y->end);
}

static int64_t find_min_arrow_shots(const Balloon *points, size_t n) {
    Balloon *sorted = malloc(n * sizeof(Balloon));
    memcpy(sorted, points, n * sizeof(Balloon));
    qsort(sorted, n, sizeof(Balloon), by_end);
    int64_t arrows = 0, arrow = 0;
    for (size_t i = 0; i < n; i++) {
        if (arrows == 0 || sorted[i].start > arrow) {
            arrows++;
            arrow = sorted[i].end;
        }
    }
    free(sorted);
    return arrows;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    enum { SETS = 10, N = 100000, ROUNDS = 10 };
    int64_t seed = 452;
    Balloon *all[SETS];
    for (int s = 0; s < SETS; s++) {
        all[s] = malloc(N * sizeof(Balloon));
        for (int i = 0; i < N; i++) {
            int64_t r = next_random(&seed) * 65536;
            r = (r + next_random(&seed)) * 2;
            r += next_random(&seed) % 2;
            int64_t start = r - 2147483648;
            int64_t w = next_random(&seed) * 65536;
            w = (w + next_random(&seed)) % 100000;
            int64_t end = start + w < 2147483647 ? start + w : 2147483647;
            all[s][i].start = start;
            all[s][i].end = end;
        }
    }
    int64_t total = 0, checksum = 0;
    for (int round = 0; round < ROUNDS; round++) {
        for (int s = 0; s < SETS; s++) {
            int64_t arrows = find_min_arrow_shots(all[s], N);
            total += arrows;
            checksum = (checksum * 31 + arrows) % 1000000007;
        }
    }
    for (int s = 0; s < SETS; s++) {
        free(all[s]);
    }
    printf("%d rounds on %d sets of %d: %lld arrows, checksum %lld\n", ROUNDS, SETS, N, (long long)total,
           (long long)checksum);
    return 0;
}
