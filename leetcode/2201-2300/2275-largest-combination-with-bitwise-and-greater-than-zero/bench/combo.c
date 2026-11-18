// LeetCode #2275: Largest Combination With Bitwise AND Greater Than Zero
// -- the bench, the ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t largest_combination(const int64_t *candidates, int64_t n) {
    int64_t best = 0;
    for (int bit = 0; bit < 24; bit++) {
        int64_t count = 0;
        for (int64_t i = 0; i < n; i++) {
            if ((candidates[i] >> bit) & 1) count++;
        }
        if (count > best) best = count;
    }
    return best;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2275;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0;
    for (int t = 0; t < 100; t++) {
        int64_t *candidates = malloc(100000 * sizeof(int64_t));
        for (int i = 0; i < 100000; i++) {
            int64_t high = next_random();
            candidates[i] = (high * 32768 + next_random()) % 10000000 + 1;
        }
        check = (check * 31 + largest_combination(candidates, 100000)) % 1000000007;
        free(candidates);
    }
    printf("100 lists of 10^5: checksum %lld\n", (long long)check);
    return 0;
}
