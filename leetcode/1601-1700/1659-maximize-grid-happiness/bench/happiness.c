// LeetCode #1659: Maximize Grid Happiness -- the bench's C mirror: the ★
// arm on 2000 random problems on grids of 4 to 5 rows by 4 to 5 columns
// with up to 6 introverts and 6 extroverts, all drawn first.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define INTROVERT 1
#define EXTROVERT 2

static int64_t pair(int64_t a, int64_t b) {
    if (a == 0 || b == 0) return 0;
    return (a == INTROVERT ? -30 : 20) + (b == INTROVERT ? -30 : 20);
}

typedef struct {
    int64_t m, n, top;
    int64_t *memo;
} Grid;

static int64_t best(Grid *g, int64_t cell, int64_t introverts, int64_t extroverts, int64_t last) {
    if (cell == g->m * g->n || (introverts == 0 && extroverts == 0)) return 0;
    int64_t key = ((cell * 7 + introverts) * 7 + extroverts) * g->top + last;
    if (g->memo[key] >= 0) return g->memo[key];
    int64_t up = last / (g->top / 3);
    int64_t left = cell % g->n == 0 ? 0 : last % 3;
    int64_t shifted = last % (g->top / 3) * 3;
    int64_t result = best(g, cell + 1, introverts, extroverts, shifted);
    if (introverts > 0) {
        int64_t gain = 120 + pair(INTROVERT, up) + pair(INTROVERT, left);
        int64_t v = gain + best(g, cell + 1, introverts - 1, extroverts, shifted + INTROVERT);
        if (v > result) result = v;
    }
    if (extroverts > 0) {
        int64_t gain = 40 + pair(EXTROVERT, up) + pair(EXTROVERT, left);
        int64_t v = gain + best(g, cell + 1, introverts, extroverts - 1, shifted + EXTROVERT);
        if (v > result) result = v;
    }
    g->memo[key] = result;
    return result;
}

static int32_t get_max_grid_happiness(int32_t m, int32_t n, int32_t introverts, int32_t extroverts) {
    int64_t top = 1;
    for (int i = 0; i < n; i++) top *= 3;
    int64_t size = (int64_t)m * n * 49 * top;
    Grid g = {m, n, top, malloc(sizeof(int64_t) * size)};
    for (int64_t i = 0; i < size; i++) g.memo[i] = -1;
    int32_t answer = (int32_t)best(&g, 0, introverts, extroverts, 0);
    free(g.memo);
    return answer;
}

static int64_t seed = 1659;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t problems[2000][4];
    for (int p = 0; p < 2000; p++) {
        problems[p][0] = (int32_t)(next_random() % 2 + 4);
        problems[p][1] = (int32_t)(next_random() % 2 + 4);
        problems[p][2] = (int32_t)(next_random() % 7);
        problems[p][3] = (int32_t)(next_random() % 7);
    }
    int64_t check = 0, total = 0;
    for (int p = 0; p < 2000; p++) {
        int64_t answer = get_max_grid_happiness(problems[p][0], problems[p][1], problems[p][2], problems[p][3]);
        total += answer;
        check = (check * 31 + answer + 1) % 1000000007;
    }
    printf("2000 grids of 4 to 5 by 4 to 5: happiness sums to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
