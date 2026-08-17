/* LeetCode 281 bench mirror — C. Same cursor iterator, same skip scan. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#define K 64
#define ROUNDS 2200
static int64_t *lists[K]; static int64_t lens[K];
static int64_t drain_sink(void) {
    int64_t cursor[K] = {0}, remaining = 0;
    for (int i = 0; i < K; i++) remaining += lens[i];
    int64_t turn = 0, tried = 0;
    while (tried < K && cursor[turn] >= lens[turn]) { turn = (turn + 1) % K; tried++; }
    int64_t h = 0, pos = 1;
    while (remaining > 0) {
        int64_t t = turn;
        int64_t v = lists[t][cursor[t]];
        cursor[t]++; remaining--;
        h = (h * 31 + v * pos) % 1000000007LL; pos++;
        turn = (t + 1) % K;
        int64_t scan = 0;
        while (scan < K && cursor[turn] >= lens[turn]) { turn = (turn + 1) % K; scan++; }
    }
    return h;
}
int main(void) {
    int64_t seed = 20260819;
    for (int i = 0; i < K; i++) {
        seed = (seed*1103515245LL+12345LL)%2147483648LL;
        int64_t len = 1 + (seed/7) % 2000;
        lens[i] = len; lists[i] = malloc((size_t)len*sizeof(int64_t));
        for (int64_t j = 0; j < len; j++) { seed = (seed*1103515245LL+12345LL)%2147483648LL; lists[i][j] = seed % 100003LL; }
    }
    int64_t sink = 0;
    for (int r = 0; r < ROUNDS; r++) sink = (sink + drain_sink()) % 1000000007LL;
    printf("%lld\n", (long long)sink);
    return 0;
}
