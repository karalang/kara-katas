// LeetCode #2410: Maximum Matching of Players With Trainers -- the bench,
// the ★ arm in C: both lists copied and sorted with `qsort`, each trainer
// upward taking the weakest player not yet matched if it is strong enough.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100000

static int64_t seed = 2410;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int ascending(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t match_players_and_trainers(const int64_t *players, const int64_t *trainers, int64_t n, int64_t m) {
    int64_t *p = malloc(n * sizeof *p), *t = malloc(m * sizeof *t);
    memcpy(p, players, n * sizeof *p);
    memcpy(t, trainers, m * sizeof *t);
    qsort(p, n, sizeof *p, ascending);
    qsort(t, m, sizeof *t, ascending);
    int64_t matched = 0;
    for (int64_t j = 0; j < m; j++)
        if (matched < n && p[matched] <= t[j]) matched++;
    free(p);
    free(t);
    return matched;
}

int main(void) {
    static int64_t players[10][N], trainers[10][N];
    for (int64_t i = 0; i < 10; i++) {
        for (int j = 0; j < N; j++) players[i][j] = 1 + (next_random() * 32768 + next_random()) % 1000000000;
        for (int j = 0; j < N; j++) trainers[i][j] = 1 + (next_random() * 32768 + next_random()) % 900000000 + 10000000 * i;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 5; p++)
        for (int i = 0; i < 10; i++) check = (check * 31 + match_players_and_trainers(players[i], trainers[i], N, N) + p) % 1000000007;
    printf("5 passes over 10 cases of 10^5 players and trainers: checksum %lld\n", (long long)check);
    return 0;
}
