// Benchmark for #568: C mirror of the ★ arm (dynamic programming over
// the weeks); see max_vacation_days.kara. The tables are rows of
// `malloc`'d arrays, and each week's `next` a fresh array, as the Kāra
// arm makes a fresh `Vec` each week.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t max_vacation_days(int64_t **flights, int64_t **days, int64_t n, int64_t k) {
    int64_t *best = malloc((size_t)n * sizeof(int64_t));
    for (int64_t c = 0; c < n; c++) {
        best[c] = -1;
    }
    best[0] = 0;
    for (int64_t w = 0; w < k; w++) {
        int64_t *next = malloc((size_t)n * sizeof(int64_t));
        for (int64_t c = 0; c < n; c++) {
            next[c] = -1;
        }
        for (int64_t j = 0; j < n; j++) {
            for (int64_t i = 0; i < n; i++) {
                if (best[i] >= 0 && (i == j || flights[i][j] == 1)) {
                    int64_t offer = best[i] + days[j][w];
                    if (offer > next[j]) {
                        next[j] = offer;
                    }
                }
            }
        }
        free(best);
        best = next;
    }
    int64_t answer = best[0];
    for (int64_t c = 1; c < n; c++) {
        if (best[c] > answer) {
            answer = best[c];
        }
    }
    free(best);
    return answer;
}

// ---- benchmark --------------------------------------------------------------

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t count = 20;
    int64_t rounds = 30;
    int64_t densities[7] = {1, 2, 5, 10, 25, 50, 100};
    int64_t seed = 568;
    int64_t **flights[20];
    int64_t **days[20];
    for (int64_t g = 0; g < count; g++) {
        int64_t density = densities[g % 7];
        flights[g] = malloc(100 * sizeof(int64_t *));
        for (int64_t i = 0; i < 100; i++) {
            flights[g][i] = calloc(100, sizeof(int64_t));
            for (int64_t j = 0; j < 100; j++) {
                if (i != j && step(&seed) % 100 < density) {
                    flights[g][i][j] = 1;
                }
            }
        }
        days[g] = malloc(100 * sizeof(int64_t *));
        for (int64_t c = 0; c < 100; c++) {
            days[g][c] = malloc(100 * sizeof(int64_t));
            for (int64_t w = 0; w < 100; w++) {
                days[g][c][w] = step(&seed) % 8;
            }
        }
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int64_t g = 0; g < count; g++) {
            int64_t p = (round * 7 + g) % count;
            int64_t got = max_vacation_days(flights[p], days[p], 100, 100);
            total += got;
            checksum = (checksum * 31 + got + 1) % 1000000007;
        }
    }
    printf("%lld cases of 100 cities and 100 weeks, %lld rounds: %lld days, checksum %lld\n",
           (long long)count, (long long)rounds, (long long)total, (long long)checksum);
    for (int64_t g = 0; g < count; g++) {
        for (int64_t i = 0; i < 100; i++) {
            free(flights[g][i]);
            free(days[g][i]);
        }
        free(flights[g]);
        free(days[g]);
    }
    return 0;
}
