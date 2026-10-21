// Benchmark for #837: New 21 Game -- the ★ arm (forward, with a sliding window).
//
// Mirrors new21_game.kara: p[i] is the chance that Alice's points are ever
// exactly i, the sum over max_pts of the chances of the totals in the last
// max_pts below i at which she still draws, kept in a running window. As
// in the Kāra program, the list of chances is a fresh allocation per call.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static double new21_game(int64_t n, int64_t k, int64_t max_pts) {
    if (k == 0 || n >= k - 1 + max_pts) return 1.0;
    double w = (double)max_pts;
    double *p = calloc((size_t)(n + 1), sizeof(double));
    p[0] = 1.0;
    double window = 1.0, answer = 0.0;
    for (int64_t i = 1; i < n + 1; i++) {
        p[i] = window / w;
        if (i < k)
            window += p[i];
        else
            answer += p[i];
        int64_t gone = i - max_pts;
        if (gone >= 0 && gone < k) window -= p[gone];
    }
    free(p);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    // 64 games drawn once, each with n from 5000 to 10^4, k from n / 2 to
    // n, and maxPts large enough that Alice can go past n, so that no game
    // takes the early return. Each round plays the next game.
    enum { COUNT = 64 };
    const int64_t rounds = 25000;
    int64_t seed = 837;
    int64_t games[COUNT][3];
    for (int64_t g = 0; g < COUNT; g++) {
        int64_t n = 5000 + next_random(&seed) % 5001;
        int64_t k = n / 2 + next_random(&seed) % (n - n / 2 + 1);
        int64_t least = n - k + 2;
        int64_t max_pts = least + next_random(&seed) % (10001 - least);
        games[g][0] = n;
        games[g][1] = k;
        games[g][2] = max_pts;
    }
    double sum = 0.0;
    for (int64_t round = 0; round < rounds; round++) {
        const int64_t *g = games[round % COUNT];
        sum += new21_game(g[0], g[1], g[2]);
    }
    printf("%lld rounds of %d games: sum %.6f\n", (long long)rounds, COUNT, sum);
    return 0;
}
