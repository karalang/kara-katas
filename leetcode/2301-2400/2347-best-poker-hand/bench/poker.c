// LeetCode #2347: Best Poker Hand -- the bench, the ★ arm in C: a flush
// when every suit equals the first; otherwise the most cards of one rank,
// counted in a table of 14, names the hand. The names are static strings,
// so no call allocates.

#include <stdint.h>
#include <stdio.h>
#include <string.h>

static const char *best_hand(const int64_t *ranks, const char *suits) {
    int flush = 1;
    for (int i = 0; i < 5; i++)
        if (suits[i] != suits[0]) flush = 0;
    if (flush) return "Flush";
    int64_t count[14] = {0};
    int64_t most = 0;
    for (int i = 0; i < 5; i++) {
        count[ranks[i]] += 1;
        if (count[ranks[i]] > most) most = count[ranks[i]];
    }
    if (most >= 3) return "Three of a Kind";
    if (most == 2) return "Pair";
    return "High Card";
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245LL + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t ranks[100000][5];
static char suits[100000][5];

int main(void) {
    // five different cards of 52, any card already in the hand drawn
    // again
    int64_t seed = 2347;
    for (int64_t h = 0; h < 100000; h++) {
        int64_t cards[5];
        int n = 0;
        while (n < 5) {
            int64_t card = next_random(&seed) % 52;
            int seen = 0;
            for (int i = 0; i < n; i++)
                if (cards[i] == card) seen = 1;
            if (!seen) cards[n++] = card;
        }
        for (int k = 0; k < 5; k++) {
            ranks[h][k] = cards[k] % 13 + 1;
            suits[h][k] = (char)(97 + cards[k] / 13);
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 30; p++)
        for (int h = 0; h < 100000; h++)
            check = (check * 31 + (int64_t)strlen(best_hand(ranks[h], suits[h])) + p) % 1000000007;
    printf("30 passes over 10^5 hands: checksum %lld\n", (long long)check);
    return 0;
}
