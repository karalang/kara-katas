// Benchmark for #518: C mirror of the ★ arm (one row, coins on the
// outside); see change.kara. The row is a fresh array for every call,
// as the ★ arm's `vec![0; amount + 1]`.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t change(int64_t amount, const int64_t *coins, int64_t n) {
    int64_t *ways = calloc(amount + 1, sizeof(int64_t));
    ways[0] = 1;
    for (int64_t i = 0; i < n; i++)
        for (int64_t a = coins[i]; a <= amount; a++) ways[a] += ways[a - coins[i]];
    int64_t answer = ways[amount];
    free(ways);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // 3,000 random sets of 100 different coins from 500 to 5,000, each
    // with an amount from 4,000 to 5,000 (the problem's most), solved
    // once each. Coins of at least 500 keep every count well inside an
    // int64_t.
    int64_t seed = 518, sets = 3000, checksum = 0;
    int64_t coins[100];
    for (int64_t s = 0; s < sets; s++) {
        int64_t amount = 4000 + next_random(&seed) % 1001;
        bool taken[5001] = {false};
        int64_t n = 0;
        while (n < 100) {
            int64_t c = 500 + next_random(&seed) % 4501;
            if (!taken[c]) {
                taken[c] = true;
                coins[n++] = c;
            }
        }
        checksum = (checksum * 31 + change(amount, coins, 100) % 1000000007) % 1000000007;
    }
    printf("%lld sets of 100 coins: checksum %lld\n", (long long)sets, (long long)checksum);
    return 0;
}
