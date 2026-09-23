// Benchmark mirror of LeetCode #322 — same bottom-up table as
// bench/coin_change.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define AMOUNT 1000000
#define COINS 20
#define TOP 3000
#define PASSES 24
#define STRIDE 9973
#define MODULUS 1073741789LL

static int64_t next(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t draw(int64_t *seed, int64_t bound) {
    int64_t hi = next(seed);
    int64_t lo = next(seed);
    return (hi * 32768 + lo) % bound;
}

static int64_t fewest(const int64_t *coins, int64_t ncoins, int64_t amount, int64_t *best) {
    int64_t unreachable = amount + 1;
    best[0] = 0;
    for (int64_t a = 1; a <= amount; a++) {
        int64_t b = unreachable;
        for (int64_t i = 0; i < ncoins; i++) {
            int64_t c = coins[i];
            if (c <= a && best[a - c] + 1 < b) {
                b = best[a - c] + 1;
            }
        }
        best[a] = b;
    }
    if (best[amount] == unreachable) return -1;
    return best[amount];
}

int main(void) {
    int64_t seed = 322;
    int64_t sink = 0;
    int64_t reached = 0;
    int64_t *best = calloc(AMOUNT + 1, sizeof(int64_t));
    int64_t coins[COINS];

    for (int64_t p = 0; p < PASSES; p++) {
        int64_t g = 1 + p % 3;
        int64_t n = 0;
        while (n < COINS) {
            int64_t c = g * (draw(&seed, TOP / g) + 1);
            int dup = 0;
            for (int64_t i = 0; i < n; i++) {
                if (coins[i] == c) { dup = 1; break; }
            }
            if (!dup) coins[n++] = c;
        }
        int64_t amount = AMOUNT / 2 + draw(&seed, AMOUNT / 2 + 1);
        int64_t ans = fewest(coins, n, amount, best);
        if (ans >= 0) reached++;
        int64_t probe = 0;
        for (int64_t a = 0; a <= amount; a += STRIDE) {
            probe = (probe * 31 + best[a]) % MODULUS;
        }
        sink = (sink * 131 + ans + 1 + probe) % MODULUS;
    }

    printf("sink %lld reached %lld\n", (long long)sink, (long long)reached);
    free(best);
    return 0;
}
