// LeetCode #2087: Minimum Cost Homecoming of a Robot in a Grid -- C mirror
// of the ★ arm's benchmark (homecoming.kara): the same grid and 2000 trips,
// each the two ranges of costs summed over a pointer and a length.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 1000000

static int64_t seed = 2087;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t sum(const int64_t *costs, int64_t len) {
    int64_t s = 0;
    for (int64_t i = 0; i < len; i++) s += costs[i];
    return s;
}

static int64_t walk(const int64_t *costs, int64_t from, int64_t to) {
    if (from < to) return sum(costs + from + 1, to - from);
    return sum(costs + to, from - to);
}

static int64_t min_cost(const int64_t *start, const int64_t *home, const int64_t *rows, const int64_t *cols) {
    return walk(rows, start[0], home[0]) + walk(cols, start[1], home[1]);
}

static int64_t place(void) {
    int64_t hi = next_random();
    return (hi * 32768 + next_random()) % N;
}

int main(void) {
    int64_t *rows = malloc(N * sizeof(int64_t));
    int64_t *cols = malloc(N * sizeof(int64_t));
    for (int i = 0; i < N; i++) rows[i] = next_random() % 10001;
    for (int i = 0; i < N; i++) cols[i] = next_random() % 10001;
    int64_t total = 0, check = 0;
    for (int k = 0; k < 2000; k++) {
        int64_t start[2], home[2];
        start[0] = place();
        start[1] = place();
        home[0] = place();
        home[1] = place();
        int64_t a = min_cost(start, home, rows, cols);
        total += a;
        check = (check * 31 + a) % 1000000007;
    }
    printf("2000 trips: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    free(rows);
    free(cols);
    return 0;
}
