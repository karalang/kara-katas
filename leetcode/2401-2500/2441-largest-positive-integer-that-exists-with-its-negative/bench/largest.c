// LeetCode #2441: Largest Positive Integer That Exists With Its Negative
// -- the bench, the ★ arm: a table of 2001 flags, offset by 1000, and
// the largest magnitude whose negative was seen. The table is allocated
// for each answer, as the other languages' are.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t find_max_k(const int64_t *nums, int64_t n) {
    bool *seen = calloc(2001, sizeof(bool));
    int64_t best = -1;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        if (seen[1000 - x]) {
            int64_t a = x < 0 ? -x : x;
            if (a > best) best = a;
        }
        seen[1000 + x] = true;
    }
    free(seen);
    return best;
}

static int64_t seed = 2441;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t nonzero(void) {
    int64_t v = 1 + next_random() % 1000;
    return next_random() % 2 == 0 ? v : -v;
}

int main(void) {
    int64_t *arrays[100];
    for (int c = 0; c < 100; c++) {
        arrays[c] = malloc(1000 * sizeof(int64_t));
        for (int i = 0; i < 1000; i++) arrays[c][i] = nonzero();
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 1000; p++)
        for (int64_t c = 0; c < 100; c++) {
            int64_t at = (p * 7919 + c * 104729) % 1000;
            arrays[c][at] = nonzero();
            check = (check * 31 + find_max_k(arrays[c], 1000) + p) % 1000000007;
        }
    printf("1000 passes over 100 arrays of 1000 values: checksum %lld\n", (long long)check);
    for (int c = 0; c < 100; c++) free(arrays[c]);
    return 0;
}
