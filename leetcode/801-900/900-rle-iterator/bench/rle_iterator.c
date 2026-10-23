// LeetCode #900: RLE Iterator -- bench program, C.
//
// The offset arm (the encoding left as it is) over one encoding of
// 200,000 runs of 1 to 1,000 terms with values up to 10^9, built once. Each
// round hands the encoding to a fresh iterator, asks for 1 to 1,000 terms
// at a time until the iterator answers -1, folds the answers into a
// checksum, and changes one run's count.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *encoding;
    int64_t len;
    int64_t i;
    int64_t used;
} RLEIterator;

static RLEIterator rle_new(int64_t *encoding, int64_t len) {
    RLEIterator it = {encoding, len, 0, 0};
    return it;
}

static int64_t rle_next(RLEIterator *it, int64_t n) {
    int64_t need = n;
    while (it->i < it->len) {
        int64_t left = it->encoding[it->i] - it->used;
        if (left >= need) {
            it->used += need;
            return it->encoding[it->i + 1];
        }
        need -= left;
        it->i += 2;
        it->used = 0;
    }
    return -1;
}

static int64_t seed = 900;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t runs = 200000;
    int64_t rounds = 140;
    int64_t *encoding = malloc(sizeof(int64_t) * 2 * runs);
    for (int64_t j = 0; j < runs; j++) {
        encoding[2 * j] = 1 + next_random() % 1000;
        int64_t hi = next_random();
        int64_t lo = next_random();
        encoding[2 * j + 1] = (hi * 32768 + lo) % 1000000001;
    }
    int64_t check = 0;
    int64_t calls = 0;
    for (int64_t round = 0; round < rounds; round++) {
        RLEIterator it = rle_new(encoding, 2 * runs);
        for (;;) {
            int64_t got = rle_next(&it, 1 + next_random() % 1000);
            calls += 1;
            if (got == -1) {
                break;
            }
            check = (check * 31 + got) % 1000000007;
        }
        encoding[2 * (round * 7919 % runs)] = 1 + next_random() % 1000;
    }
    printf("%lld rounds over %lld runs: %lld calls, checksum %lld\n", (long long)rounds,
           (long long)runs, (long long)calls, (long long)check);
    free(encoding);
    return 0;
}
