// LeetCode #2158: Amount of New Area Painted Each Day -- the benchmark's C
// mirror of painted.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define DAYS 100000

static int64_t seed = 2158;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static void segment(int64_t *p) {
    int64_t length = wide_random() % 500 + 1;
    int64_t start = wide_random() % (50000 - length + 1);
    p[0] = start;
    p[1] = start + length;
}

static int64_t first_unpainted(int64_t *next, int64_t x) {
    while (next[x] != x) {
        next[x] = next[next[x]];
        x = next[x];
    }
    return x;
}

static void amount_painted(int64_t (*paint)[2], int64_t n, int64_t *log) {
    int64_t wall = 0;
    for (int64_t i = 0; i < n; i++) {
        if (paint[i][1] > wall) {
            wall = paint[i][1];
        }
    }
    int64_t *next = malloc((size_t)(wall + 1) * sizeof(int64_t));
    for (int64_t x = 0; x <= wall; x++) {
        next[x] = x;
    }
    for (int64_t i = 0; i < n; i++) {
        int64_t painted = 0;
        int64_t x = first_unpainted(next, paint[i][0]);
        while (x < paint[i][1]) {
            painted++;
            next[x] = x + 1;
            x = first_unpainted(next, x + 1);
        }
        log[i] = painted;
    }
    free(next);
}

static int64_t lists[4][DAYS][2];

int main(void) {
    for (int l = 0; l < 4; l++) {
        for (int64_t i = 0; i < DAYS; i++) {
            segment(lists[l][i]);
        }
    }
    int64_t *log = malloc(DAYS * sizeof(int64_t));
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 5; round++) {
        for (int l = 0; l < 4; l++) {
            int64_t at = wide_random() % DAYS;
            segment(lists[l][at]);
            amount_painted(lists[l], DAYS, log);
            for (int64_t day = 0; day < DAYS; day++) {
                total += log[day];
                check = (check * 31 + log[day] * (day + 1) + round) % 1000000007;
            }
        }
    }
    printf("20 solves: %lld units in all, checksum %lld\n", (long long)total, (long long)check);
    free(log);
    return 0;
}
