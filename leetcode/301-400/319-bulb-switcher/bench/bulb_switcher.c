/* Benchmark mirror of LeetCode #319 — the round simulation.
   Same algorithm as bench/bulb_switcher.kara: PASSES passes, each simulating
   n rounds over an n-bulb byte array and folding the count of lit bulbs
   together with the sum of their indices. */
#include <stdio.h>
#include <stdlib.h>

#define BULBS   6000000LL
#define PASSES  10LL
#define STRIDE  90011LL
#define MASKMOD 1073741823LL

int main(void) {
    unsigned char *on = calloc(BULBS + 1, 1);
    if (!on) return 1;

    long long sink = 0;
    for (long long p = 0; p < PASSES; p++) {
        long long n = BULBS - p * STRIDE;

        for (long long b = 0; b <= n; b++) on[b] = 0;

        for (long long step = 1; step <= n; step++)
            for (long long b = step; b <= n; b += step)
                on[b] ^= 1;

        long long count = 0, idx_sum = 0;
        for (long long b = 1; b <= n; b++) {
            if (on[b] == 1) {
                count++;
                idx_sum = (idx_sum + b) % MASKMOD;
            }
        }
        sink = (sink * 31 + count * 7919 + idx_sum) % MASKMOD;
    }

    printf("checksum %lld\n", sink);
    free(on);
    return 0;
}
