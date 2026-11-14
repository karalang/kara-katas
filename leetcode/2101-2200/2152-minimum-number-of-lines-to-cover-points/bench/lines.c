// LeetCode #2152: Minimum Number of Lines to Cover Points -- the
// benchmark's C mirror of lines.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 10

static int64_t minimum_lines(int64_t points[N][2], int64_t n) {
    int64_t full = ((int64_t)1 << n) - 1;
    int64_t *fewest = malloc(sizeof(int64_t) * ((size_t)1 << n));
    for (int64_t m = 0; m <= full; m++) fewest[m] = n + 1;
    fewest[0] = 0;
    for (int64_t mask = 0; mask < full; mask++) {
        if (fewest[mask] > n) continue;
        int64_t i = 0;
        while ((mask >> i) & 1) i++;
        int64_t alone = mask | ((int64_t)1 << i);
        if (fewest[mask] + 1 < fewest[alone]) fewest[alone] = fewest[mask] + 1;
        for (int64_t j = i + 1; j < n; j++) {
            int64_t line = 0;
            for (int64_t k = 0; k < n; k++) {
                int64_t cross = (points[j][0] - points[i][0]) * (points[k][1] - points[i][1]) - (points[j][1] - points[i][1]) * (points[k][0] - points[i][0]);
                if (cross == 0) line |= (int64_t)1 << k;
            }
            if (fewest[mask] + 1 < fewest[mask | line]) fewest[mask | line] = fewest[mask] + 1;
        }
    }
    int64_t best = fewest[full];
    free(fewest);
    return best;
}

static int64_t seed = 2152;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void free_place(int64_t points[N][2], int64_t count, int64_t out[2]) {
    for (;;) {
        int64_t x = next_random() % 7 - 3;
        int64_t y = next_random() % 7 - 3;
        int taken = 0;
        for (int64_t k = 0; k < count; k++) {
            if (points[k][0] == x && points[k][1] == y) taken = 1;
        }
        if (!taken) {
            out[0] = x;
            out[1] = y;
            return;
        }
    }
}

static int64_t sets[4][N][2];

int main(void) {
    for (int s = 0; s < 4; s++) {
        for (int64_t k = 0; k < N; k++) free_place(sets[s], k, sets[s][k]);
    }
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t round = 0; round < 2500; round++) {
        for (int s = 0; s < 4; s++) {
            int64_t at = next_random() % 10;
            int64_t p[2];
            free_place(sets[s], N, p);
            sets[s][at][0] = p[0];
            sets[s][at][1] = p[1];
            int64_t lines = minimum_lines(sets[s], N);
            total += lines;
            check = (check * 31 + lines + round) % 1000000007;
        }
    }
    printf("10000 solves: %lld lines in all, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
