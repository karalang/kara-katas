// LeetCode #1291 bench: the ★ arm over 10^5 ranges built once, then 20
// passes, each moving every range's low up by the checksum so far, answering
// it, and folding the count and the numbers found into the checksum. The
// answer goes into a fresh allocation per call, as the other languages'
// growable arrays do.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t *sequential_digits(int64_t low, int64_t high, int *count) {
    int64_t *found = malloc(sizeof(int64_t) * 36);
    int n = 0;
    for (int len = 2; len < 10; len++) {
        for (int first = 1; first < 11 - len; first++) {
            int64_t x = 0;
            for (int d = first; d < first + len; d++) {
                x = x * 10 + d;
            }
            if (x >= low && x <= high) {
                found[n++] = x;
            }
        }
    }
    *count = n;
    return found;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t wide_random(int64_t *seed) {
    int64_t a = next_random(seed);
    return a * 32768 + next_random(seed);
}

int main(void) {
    enum { RANGES = 100000 };
    int64_t seed = 1291;
    int64_t *lows = malloc(sizeof(int64_t) * RANGES);
    int64_t *highs = malloc(sizeof(int64_t) * RANGES);
    for (int a = 0; a < RANGES; a++) {
        int64_t base = 10;
        for (int64_t k = next_random(&seed) % 8; k > 0; k--) {
            base *= 10;
        }
        int64_t span = 1;
        for (int64_t k = next_random(&seed) % 10; k > 0; k--) {
            span *= 10;
        }
        int64_t low = base + wide_random(&seed) % (9 * base);
        int64_t high = low + wide_random(&seed) % span;
        lows[a] = low;
        highs[a] = high > 1000000000 ? 1000000000 : high;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 20; p++) {
        for (int a = 0; a < RANGES; a++) {
            int64_t moved = lows[a] + check % 1000;
            int count;
            int64_t *found = sequential_digits(moved > highs[a] ? highs[a] : moved, highs[a], &count);
            check = (check * 31 + count + p) % 1000000007;
            for (int i = 0; i < count; i++) {
                check = (check * 131 + found[i]) % 1000000007;
            }
            free(found);
        }
    }
    printf("20 passes over 10^5 ranges: checksum %lld\n", (long long)check);
    return 0;
}
