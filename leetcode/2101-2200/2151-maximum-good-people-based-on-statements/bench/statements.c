// LeetCode #2151: Maximum Good People Based on Statements -- the
// benchmark's C mirror of statements.kara.

#include <stdint.h>
#include <stdio.h>

#define N 15

static int64_t maximum_good(int64_t statements[N][N], int64_t n) {
    int64_t best = 0;
    for (int64_t mask = 0; mask < ((int64_t)1 << n); mask++) {
        int holds = 1;
        for (int64_t i = 0; i < n; i++) {
            if ((mask >> i) & 1) {
                for (int64_t j = 0; j < n; j++) {
                    int64_t say = statements[i][j];
                    if (say != 2 && say != ((mask >> j) & 1)) {
                        holds = 0;
                    }
                }
            }
        }
        if (holds) {
            int64_t good = __builtin_popcountll((unsigned long long)mask);
            if (good > best) best = good;
        }
    }
    return best;
}

static int64_t seed = 2151;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t villages[4][N][N];

int main(void) {
    for (int v = 0; v < 4; v++) {
        int64_t hidden = next_random() % (1 << N);
        for (int64_t i = 0; i < N; i++) {
            for (int64_t j = 0; j < N; j++) {
                int64_t say;
                if (i == j) {
                    say = 2;
                } else if ((hidden >> i) & 1) {
                    say = next_random() % 3 == 0 ? 2 : (hidden >> j) & 1;
                } else {
                    say = next_random() % 3;
                }
                villages[v][i][j] = say;
            }
        }
    }
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t round = 0; round < 25; round++) {
        for (int v = 0; v < 4; v++) {
            int64_t i = next_random() % N;
            int64_t j = (i + 1 + next_random() % (N - 1)) % N;
            villages[v][i][j] = next_random() % 3;
            int64_t good = maximum_good(villages[v], N);
            total += good;
            check = (check * 31 + good + round) % 1000000007;
        }
    }
    printf("100 solves: %lld good in all, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
