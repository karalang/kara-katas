// LeetCode #1637: Widest Vertical Area Between Two Points Containing No
// Points -- the bench's C mirror: the ★ arm on 40 random sets of 100000
// points with x and y from 0 to 10^9, all drawn first, each point its own
// two-int allocation as LeetCode's int** hands them over.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

enum { SETS = 40, N = 100000 };

static int by_value(const void *x, const void *y) {
    int32_t a = *(const int32_t *)x, b = *(const int32_t *)y;
    return (a > b) - (a < b);
}

static int32_t max_width_of_vertical_area(int32_t **points, size_t n) {
    int32_t *xs = malloc(sizeof(int32_t) * n);
    for (size_t i = 0; i < n; i++) xs[i] = points[i][0];
    qsort(xs, n, sizeof(int32_t), by_value);
    int32_t widest = 0;
    for (size_t i = 1; i < n; i++)
        if (xs[i] - xs[i - 1] > widest) widest = xs[i] - xs[i - 1];
    free(xs);
    return widest;
}

static int64_t seed = 1637;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int32_t **sets[SETS];
    for (int s = 0; s < SETS; s++) {
        sets[s] = malloc(sizeof(int32_t *) * N);
        for (int i = 0; i < N; i++) {
            int64_t x = (next_random() * 32768 + next_random()) % 1000000001;
            int64_t y = (next_random() * 32768 + next_random()) % 1000000001;
            sets[s][i] = malloc(sizeof(int32_t) * 2);
            sets[s][i][0] = (int32_t)x;
            sets[s][i][1] = (int32_t)y;
        }
    }
    int64_t check = 0, total = 0;
    for (int s = 0; s < SETS; s++) {
        int64_t width = max_width_of_vertical_area(sets[s], N);
        total += width;
        check = (check * 31 + width + 1) % 1000000007;
    }
    for (int s = 0; s < SETS; s++) {
        for (int i = 0; i < N; i++) free(sets[s][i]);
        free(sets[s]);
    }
    printf("40 sets of 100000 points: widths sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
