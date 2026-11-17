// LeetCode #1183: Maximum Number of Ones -- the ★ arm in C: the cells on
// each position of the `side * side` square counted, sorted largest first
// with `qsort`, and the first `max_ones` summed.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int larger_first(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (y > x) - (y < x);
}

static int64_t counts[10000];

static int64_t maximum_number_of_ones(int64_t width, int64_t height, int64_t side_length, int64_t max_ones) {
    int n = 0;
    for (int64_t i = 0; i < side_length; i++) {
        for (int64_t j = 0; j < side_length; j++) {
            int64_t across = (width - i - 1) / side_length + 1;
            int64_t down = (height - j - 1) / side_length + 1;
            counts[n++] = across * down;
        }
    }
    qsort(counts, n, sizeof(int64_t), larger_first);
    int64_t total = 0;
    for (int64_t k = 0; k < max_ones; k++) total += counts[k];
    return total;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1183;
    int64_t cases[1000][4];
    for (int k = 0; k < 1000; k++) {
        int64_t width = 1 + next_random(&seed) % 100;
        int64_t height = 1 + next_random(&seed) % 100;
        int64_t side = 1 + next_random(&seed) % (width < height ? width : height);
        int64_t max_ones = next_random(&seed) % (side * side + 1);
        cases[k][0] = width; cases[k][1] = height; cases[k][2] = side; cases[k][3] = max_ones;
    }
    int rounds = 100;
    int64_t check = 0;
    for (int r = 0; r < rounds; r++)
        for (int k = 0; k < 1000; k++)
            check = (check * 131 + maximum_number_of_ones(cases[k][0], cases[k][1], cases[k][2], cases[k][3]) + r) % 1000000007;
    printf("%d rounds of 1000 cases: checksum %lld\n", rounds, (long long)check);
    return 0;
}
