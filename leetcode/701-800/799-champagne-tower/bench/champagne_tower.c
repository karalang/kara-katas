// LeetCode 799 — Champagne Tower: the bench, in C. Mirrors
// champagne_tower.kara: one row at a time, each row a fresh allocation.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static double champagne_tower(int64_t poured, int64_t query_row, int64_t query_glass) {
    double *row = malloc(sizeof(double));
    row[0] = (double)poured;
    for (int64_t r = 0; r < query_row; r++) {
        double *below = calloc(r + 2, sizeof(double));
        for (int64_t c = 0; c < r + 1; c++) {
            if (row[c] > 1.0) {
                double half = (row[c] - 1.0) / 2.0;
                below[c] += half;
                below[c + 1] += half;
            }
        }
        free(row);
        row = below;
    }
    double got = row[query_glass];
    free(row);
    return got > 1.0 ? 1.0 : got;
}

static int64_t seed = 799;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t q[4096][3];
    for (int i = 0; i < 4096; i++) {
        int64_t hi = next_random();
        q[i][0] = (hi * 32768 + next_random()) % 1000000001;
        q[i][1] = 50 + next_random() % 50;
        q[i][2] = next_random() % (q[i][1] + 1);
    }
    const int64_t rounds = 81920;
    double total = 0.0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        double got = champagne_tower(q[r % 4096][0], q[r % 4096][1], q[r % 4096][2]);
        total += got;
        check = (check * 31 + (int64_t)(got * 1000000.0)) % 1000000007;
    }
    printf("%lld glasses: %.5f cups in all, checksum %lld\n", (long long)rounds, total, (long long)check);
    return 0;
}
