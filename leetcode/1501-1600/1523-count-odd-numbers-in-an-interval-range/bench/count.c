// LeetCode #1523: Count Odd Numbers in an Interval Range -- bench: the ★
// arm over 2000000 random intervals within 0 to 10^9, built once and
// answered 100 times, each pass summed.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t count_odds(int64_t low, int64_t high) {
    return (high + 1) / 2 - low / 2;
}

static int64_t seed = 1523;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) {
    return (check * 31 + x + 1) % 1000000007;
}

int main(void) {
    enum { COUNT = 2000000 };
    int64_t *lows = malloc(COUNT * sizeof(int64_t));
    int64_t *highs = malloc(COUNT * sizeof(int64_t));
    for (int i = 0; i < COUNT; i++) {
        int64_t hi = next_random();
        int64_t a = (hi * 32768 + next_random()) % 1000000001;
        hi = next_random();
        int64_t b = (hi * 32768 + next_random()) % 1000000001;
        lows[i] = a < b ? a : b;
        highs[i] = a < b ? b : a;
    }
    int64_t check = 0;
    for (int pass = 0; pass < 100; pass++) {
        int64_t total = 0;
        for (int i = 0; i < COUNT; i++) {
            total += count_odds(lows[i], highs[i]);
        }
        check = mix(check, total % 1000000007);
    }
    printf("100 passes over 2000000 intervals within 0 to 10^9: checksum %lld\n", (long long)check);
    free(lows);
    free(highs);
    return 0;
}
