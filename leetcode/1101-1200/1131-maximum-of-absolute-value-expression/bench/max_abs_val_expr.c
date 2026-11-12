// LeetCode #1131: Maximum of Absolute Value Expression -- the bench in C,
// the same algorithm and workload as max_abs_val_expr.kara: each array
// allocated by itself, the same 8 pairs of 40000 values and 400 rounds.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t max_abs_val_expr(const int64_t *arr1, const int64_t *arr2, int64_t n) {
    static const int64_t signs[4][2] = {{1, 1}, {1, -1}, {-1, 1}, {-1, -1}};
    int64_t best = 0;
    for (int k = 0; k < 4; k++) {
        int64_t p = signs[k][0], q = signs[k][1];
        int64_t high = INT64_MIN, low = INT64_MAX;
        for (int64_t i = 0; i < n; i++) {
            int64_t v = p * arr1[i] + q * arr2[i] + i;
            if (v > high) high = v;
            if (v < low) low = v;
        }
        if (high - low > best) best = high - low;
    }
    return best;
}

static int64_t seed = 1131;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t value(void) {
    int64_t high = next_random();
    int64_t low = next_random();
    return (high * 32768 + low) % 2000001 - 1000000;
}

int main(void) {
    static int64_t *firsts[8], *seconds[8];
    for (int j = 0; j < 8; j++) {
        firsts[j] = malloc(40000 * sizeof(int64_t));
        seconds[j] = malloc(40000 * sizeof(int64_t));
        for (int i = 0; i < 40000; i++) firsts[j][i] = value();
        for (int i = 0; i < 40000; i++) seconds[j][i] = value();
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 400; round++) {
        for (int64_t j = 0; j < 8; j++) {
            int64_t at = (round * 7919 + j * 104729) % 40000;
            firsts[j][at] = ((firsts[j][at] + 1000000) * 7 + 12345) % 2000001 - 1000000;
            seconds[j][at] = ((seconds[j][at] + 1000000) * 11 + 54321) % 2000001 - 1000000;
            int64_t r = max_abs_val_expr(firsts[j], seconds[j], 40000);
            total += r;
            check = (check * 31 + r) % 1000000007;
        }
    }
    printf("400 rounds over 8 pairs of 40000 values: answers total %lld, checksum %lld\n",
           (long long)total, (long long)check);
    for (int j = 0; j < 8; j++) {
        free(firsts[j]);
        free(seconds[j]);
    }
    return 0;
}
