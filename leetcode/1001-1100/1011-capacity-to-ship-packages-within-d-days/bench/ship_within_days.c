// LeetCode #1011 bench: the ★ arm (binary search on the capacity) over 20
// rows of 50,000 packages, drawn once; each of 20 rounds ships every row,
// each call with its own number of days, and folds each capacity into a
// checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t days_needed(const int64_t *w, int64_t n, int64_t capacity) {
    int64_t used = 1, load = 0;
    for (int64_t i = 0; i < n; i++) {
        if (load + w[i] > capacity) {
            used += 1;
            load = 0;
        }
        load += w[i];
    }
    return used;
}

static int64_t ship_within_days(const int64_t *w, int64_t n, int64_t days) {
    int64_t lo = 0, hi = 0;
    for (int64_t i = 0; i < n; i++) {
        if (w[i] > lo) lo = w[i];
        hi += w[i];
    }
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (days_needed(w, n, mid) <= days) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}

static int64_t seed = 1011;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { COUNT = 20, ROUNDS = 20, N = 50000 };
    int64_t *rows = malloc((size_t)COUNT * N * sizeof(int64_t));
    for (int k = 0; k < COUNT; k++)
        for (int i = 0; i < N; i++) rows[(int64_t)k * N + i] = 1 + next_random() % 500;
    int64_t check = 0;
    for (int64_t r = 0; r < ROUNDS; r++)
        for (int64_t k = 0; k < COUNT; k++) {
            int64_t days = 1 + ((r * COUNT + k) * 7919) % 50000;
            check = (check * 31 + ship_within_days(rows + k * N, N, days)) % 1000000007;
        }
    printf("%d rounds over %d rows of 50000 packages: checksum %lld\n", ROUNDS, COUNT, (long long)check);
    free(rows);
    return 0;
}
