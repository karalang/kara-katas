// LeetCode 808 — Soup Servings: the bench.
//
// Each round works out the answer for a size from 3750 to 4800 ml, 150
// to 192 servings, the largest the table is built for.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t at_least0(int64_t x) { return x > 0 ? x : 0; }

static double soup_servings(int64_t n) {
    if (n > 4800) return 1.0;
    int64_t m = (n + 24) / 25;
    double **p = malloc((m + 1) * sizeof(double *));
    for (int64_t a = 0; a <= m; a++) p[a] = calloc(m + 1, sizeof(double));
    static const int64_t pour[4][2] = {{4, 0}, {3, 1}, {2, 2}, {1, 3}};
    for (int64_t a = 0; a <= m; a++) {
        for (int64_t b = 0; b <= m; b++) {
            if (a == 0 && b == 0) {
                p[a][b] = 0.5;
            } else if (a == 0) {
                p[a][b] = 1.0;
            } else if (b == 0) {
                p[a][b] = 0.0;
            } else {
                double sum = 0.0;
                for (int k = 0; k < 4; k++) sum += p[at_least0(a - pour[k][0])][at_least0(b - pour[k][1])];
                p[a][b] = 0.25 * sum;
            }
        }
    }
    double answer = p[m][m];
    for (int64_t a = 0; a <= m; a++) free(p[a]);
    free(p);
    return answer;
}

int main(void) {
    int64_t rounds = 30000;
    double total = 0.0;
    int64_t sure = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t n = 3750 + (r * 37) % 1051;
        double p = soup_servings(n);
        total += p;
        if (p > 0.99999) sure++;
    }
    printf("%lld rounds of 3750 to 4800 ml: sum %.6f, %lld above 0.99999\n", (long long)rounds, total,
           (long long)sure);
    return 0;
}
