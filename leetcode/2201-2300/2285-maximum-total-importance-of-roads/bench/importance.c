// LeetCode #2285: Maximum Total Importance of Roads -- the bench, the ★
// arm's C twin. The degrees sorted with `qsort`, the k-th smallest
// valued k.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int by_value(const void *x, const void *y) {
    int64_t a = *(const int64_t *)x, b = *(const int64_t *)y;
    return (a > b) - (a < b);
}

static int64_t maximum_importance(int64_t n, const int64_t (*roads)[2], int64_t m) {
    int64_t *degree = calloc((size_t)n, sizeof *degree);
    for (int64_t r = 0; r < m; r++) {
        degree[roads[r][0]]++;
        degree[roads[r][1]]++;
    }
    qsort(degree, (size_t)n, sizeof *degree, by_value);
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) total += degree[i] * (i + 1);
    free(degree);
    return total;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2285;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t (*graphs)[5000][2] = malloc(200 * sizeof *graphs);
    for (int g = 0; g < 200; g++) {
        int m = 0;
        while (m < 5000) {
            int64_t a = next_random() * 32768;
            a = (a + next_random()) % 5000;
            int64_t b = next_random() * 32768;
            b = (b + next_random()) % 5000;
            if (a != b) {
                graphs[g][m][0] = a;
                graphs[g][m][1] = b;
                m++;
            }
        }
    }
    int64_t check = 0;
    for (int p = 0; p < 20; p++) {
        for (int g = 0; g < 200; g++) {
            check = (check * 31 + maximum_importance(5000, graphs[g], 5000)) % 1000000007;
        }
    }
    free(graphs);
    printf("20 passes over 200 graphs of 5000 cities: checksum %lld\n", (long long)check);
    return 0;
}
