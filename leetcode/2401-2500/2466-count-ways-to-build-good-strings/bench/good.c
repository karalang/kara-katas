// LeetCode #2466: Count Ways To Build Good Strings -- the bench, the ★ arm
// in C: bottom-up counts in a buffer allocated for each answer, each
// length's the sum of the counts one block back, and the counts from
// `low` to `high` summed.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007

static int64_t count_good_strings(int64_t low, int64_t high, int64_t zero, int64_t one) {
    int64_t *ways = calloc(high + 1, sizeof(int64_t));
    ways[0] = 1;
    int64_t total = 0;
    for (int64_t len = 1; len <= high; len++) {
        if (len >= zero) ways[len] = (ways[len] + ways[len - zero]) % MOD;
        if (len >= one) ways[len] = (ways[len] + ways[len - one]) % MOD;
        if (len >= low) total = (total + ways[len]) % MOD;
    }
    free(ways);
    return total;
}

static int64_t seed = 2466;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t min64(int64_t a, int64_t b) { return a < b ? a : b; }

int main(void) {
    // 20 cases built once, `high` from 50000 to 10^5, `low` from 1 to
    // `high`, blocks of 1 to 20 no longer than `low`; then 28 passes,
    // each setting every case's zero block from the checksum so far, then
    // answering it and folding the answer plus the pass into the checksum
    int64_t lows[20], highs[20], zeros[20], ones[20];
    for (int i = 0; i < 20; i++) {
        int64_t r1 = next_random();
        int64_t r2 = next_random();
        highs[i] = 50000 + (r1 * 32768 + r2) % 50001;
        int64_t r3 = next_random();
        int64_t r4 = next_random();
        lows[i] = 1 + (r3 * 32768 + r4) % highs[i];
        zeros[i] = 1 + next_random() % min64(lows[i], 20);
        ones[i] = 1 + next_random() % min64(lows[i], 20);
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 28; p++) {
        for (int64_t a = 0; a < 20; a++) {
            zeros[a] = 1 + (check + a) % min64(lows[a], 20);
            check = (check * 31 + count_good_strings(lows[a], highs[a], zeros[a], ones[a]) + p) % 1000000007;
        }
    }
    printf("28 passes over 20 cases up to 10^5: checksum %lld\n", (long long)check);
    return 0;
}
