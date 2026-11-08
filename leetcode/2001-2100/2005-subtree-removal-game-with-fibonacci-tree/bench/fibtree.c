// LeetCode #2005: Subtree Removal Game with Fibonacci Tree -- the benchmark's
// C twin, the same algorithm as fibtree.kara here, the values allocated per
// call as the Kāra program does.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static bool find_game_winner(int64_t n) {
    // value[k] is order(k)'s value; value[0] is unused
    int64_t *value = calloc(n + 1, sizeof(int64_t));
    for (int64_t k = 2; k <= n; k++) {
        int64_t left = k >= 3 ? value[k - 2] + 1 : 0;
        value[k] = left ^ (value[k - 1] + 1);
    }
    bool wins = value[n] != 0;
    free(value);
    return wins;
}

static int64_t seed = 2005;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    // 500000 values of n from 1 to 100 drawn once, then the ★ arm on each, 10 rounds
    enum { Q = 500000 };
    static int64_t queries[Q];
    for (int i = 0; i < Q; i++) queries[i] = next_random() % 100 + 1;
    int64_t calls = 0, alice = 0, check = 0;
    for (int r = 0; r < 10; r++) {
        for (int i = 0; i < Q; i++) {
            int64_t n = queries[i];
            bool wins = find_game_winner(n);
            calls++;
            if (wins) alice++;
            check = (check * 31 + (wins ? n : 0)) % 1000000007;
        }
    }
    printf("%lld calls: Alice wins %lld, checksum %lld\n", (long long)calls, (long long)alice, (long long)check);
    return 0;
}
