// LeetCode #1643: Kth Smallest Instructions -- the bench's C mirror: the
// ★ arm on 1000000 random destinations of 1 to 15 rows and columns, each
// with a k drawn from all of its paths, all drawn first. The triangle and
// the path are allocated per call, as the other languages do.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CASES 1000000

static char *kth_smallest_path(const int32_t *destination, int32_t k32) {
    int64_t v = destination[0], h = destination[1];
    int64_t n = v + h;
    int64_t **choose = malloc((size_t)(n + 1) * sizeof *choose);
    for (int64_t i = 0; i <= n; i++) choose[i] = calloc((size_t)(n + 1), sizeof **choose);
    for (int64_t i = 0; i <= n; i++) {
        choose[i][0] = 1;
        for (int64_t j = 1; j <= i; j++) choose[i][j] = choose[i - 1][j - 1] + choose[i - 1][j];
    }
    int64_t k = k32;
    char *path = malloc((size_t)n + 1);
    for (int64_t s = 0; s < n; s++) {
        int64_t starting_h = choose[h + v - 1][v];
        if (k <= starting_h) {
            path[s] = 'H';
            h -= 1;
        } else {
            path[s] = 'V';
            k -= starting_h;
            v -= 1;
        }
    }
    path[n] = '\0';
    for (int64_t i = 0; i <= n; i++) free(choose[i]);
    free(choose);
    return path;
}

static int64_t seed = 1643;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t count_paths(int64_t row, int64_t column) {
    int64_t count = 1;
    for (int64_t i = 1; i <= row; i++) count = count * (column + i) / i;
    return count;
}

int main(void) {
    static int32_t drawn[CASES][3];
    for (int c = 0; c < CASES; c++) {
        int64_t row = next_random() % 15 + 1;
        int64_t column = next_random() % 15 + 1;
        int64_t a = next_random();
        int64_t b = next_random();
        int64_t k = (a * 32768 + b) % count_paths(row, column) + 1;
        drawn[c][0] = (int32_t)row;
        drawn[c][1] = (int32_t)column;
        drawn[c][2] = (int32_t)k;
    }
    int64_t check = 0, total = 0;
    for (int c = 0; c < CASES; c++) {
        char *path = kth_smallest_path(drawn[c], drawn[c][2]);
        total += strchr(path, 'V') - path;
        for (char *p = path; *p; p++) check = (check * 3 + (*p == 'H' ? 1 : 2)) % 1000000007;
        free(path);
    }
    printf("%d destinations of up to 15 by 15: first moves down sum to %lld, checksum %lld\n", CASES, (long long)total, (long long)check);
    return 0;
}
