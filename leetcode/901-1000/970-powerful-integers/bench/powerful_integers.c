// Benchmark: LeetCode #970 Powerful Integers -- the ★ arm, every pair of
// powers in a set, for every x and y from 1 to 100 with bound 10^6.
// Mirrors powerful_integers.kara, .rs, .py and go-seq/. The set is one
// open-addressing table of 1,024 slots reused across calls, each slot
// stamped with the call that filled it, so no call clears or allocates
// it; each call mallocs its powers and its answer, as the other
// languages allocate theirs.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define SLOTS 1024

static int64_t keys[SLOTS];
static int64_t stamp[SLOTS];
static int64_t call;

// The powers of base up to bound in *out, their count returned.
static int64_t powers(int64_t base, int64_t bound, int64_t **out) {
    int64_t *p = malloc(sizeof(int64_t) * 21);
    int64_t len = 0;
    for (int64_t v = 1; v <= bound; v *= base) {
        p[len++] = v;
        if (base == 1) break;
    }
    *out = p;
    return len;
}

// The powerful integers in *out, in table order, their count returned.
static int64_t powerful_integers(int64_t x, int64_t y, int64_t bound, int64_t **out) {
    call++;
    int64_t *found = malloc(sizeof(int64_t) * SLOTS);
    int64_t len = 0;
    int64_t *xs;
    int64_t nx = powers(x, bound, &xs);
    for (int64_t i = 0; i < nx; i++) {
        int64_t *ys;
        int64_t ny = powers(y, bound - xs[i], &ys);
        for (int64_t j = 0; j < ny; j++) {
            int64_t v = xs[i] + ys[j];
            uint64_t h = ((uint64_t)v * 0x9E3779B97F4A7C15ull) >> 54;
            while (stamp[h] == call && keys[h] != v) h = (h + 1) & (SLOTS - 1);
            if (stamp[h] != call) {
                stamp[h] = call;
                keys[h] = v;
                found[len++] = v;
            }
        }
        free(ys);
    }
    free(xs);
    *out = found;
    return len;
}

int main(void) {
    const int64_t rounds = 100;
    int64_t found = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t x = 1; x <= 100; x++) {
            for (int64_t y = 1; y <= 100; y++) {
                int64_t *got;
                int64_t len = powerful_integers(x, y, 1000000 - r, &got);
                for (int64_t i = 0; i < len; i++) {
                    found++;
                    check = (check + got[i] * got[i]) % 1000000007;
                }
                free(got);
            }
        }
    }
    printf("%lld rounds over x and y from 1 to 100: %lld powerful integers, checksum %lld\n", (long long)rounds,
           (long long)found, (long long)check);
    return 0;
}
