// LeetCode #2836: Maximize Value of Function in a Ball Passing Game --
// the bench, mirrored from ball.kara: binary lifting over 34 levels.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define LEVELS 34

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t wide(int64_t *seed) {
    int64_t hi = next_random(seed);
    return hi * 32768 + next_random(seed);
}

static int64_t get_max_function_value(const int64_t *receiver, int64_t n, int64_t k) {
    int64_t *jump = malloc(sizeof(int64_t) * LEVELS * n);
    int64_t *gain = malloc(sizeof(int64_t) * LEVELS * n);
    for (int64_t i = 0; i < n; i++) jump[i] = gain[i] = receiver[i];
    for (int64_t j = 1; j < LEVELS; j++) {
        const int64_t *pj = jump + (j - 1) * n, *pg = gain + (j - 1) * n;
        int64_t *nj = jump + j * n, *ng = gain + j * n;
        for (int64_t i = 0; i < n; i++) nj[i] = pj[pj[i]];
        for (int64_t i = 0; i < n; i++) ng[i] = pg[i] + pg[pj[i]];
    }
    int64_t best = 0;
    for (int64_t start = 0; start < n; start++) {
        int64_t at = start, total = start;
        for (int64_t j = 0; j < LEVELS; j++) {
            if ((k >> j) & 1) {
                total += gain[j * n + at];
                at = jump[j * n + at];
            }
        }
        if (total > best) best = total;
    }
    free(jump); free(gain);
    return best;
}

int main(void) {
    const int64_t count = 10, rounds = 3, n = 100000;
    int64_t seed = 2836;
    int64_t *receivers = malloc(sizeof(int64_t) * count * n);
    int64_t ks[10];
    for (int64_t c = 0; c < count; c++) {
        for (int64_t i = 0; i < n; i++) receivers[c * n + i] = wide(&seed) % n;
        int64_t w = wide(&seed);
        ks[c] = (w * 10 + next_random(&seed)) % 10000000000LL + 1;
    }
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t best = get_max_function_value(receivers + c * n, n, ks[c]);
            check = (check * 31 + best % 1000000007 + r) % 1000000007;
        }
    }
    printf("%lld games of %lld, %lld rounds: checksum %lld\n", (long long)count, (long long)n, (long long)rounds, (long long)check);
    free(receivers);
    return 0;
}
