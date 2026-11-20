// LeetCode #1252 bench, in C: the ★ arm (the matrix itself, every cell of
// each place's row and column raised by one, then the odd cells counted)
// on 1000 random lists of 100 places in a 50 by 50 matrix built once,
// each asked 40 times; every count folded into a checksum.

#include <stdio.h>
#include <stdlib.h>

#define CASES 1000
#define K 100

static long long seed = 1252;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long odd_cells(int m, int n, const int (*indices)[2], int k) {
    long long *matrix = calloc((size_t)m * n, sizeof(long long));
    for (int p = 0; p < k; p++) {
        int r = indices[p][0], c = indices[p][1];
        for (int j = 0; j < n; j++) matrix[r * n + j] += 1;
        for (int i = 0; i < m; i++) matrix[i * n + c] += 1;
    }
    long long odd = 0;
    for (int i = 0; i < m * n; i++)
        if (matrix[i] % 2 == 1) odd++;
    free(matrix);
    return odd;
}

static int cases[CASES][K][2];

int main(void) {
    for (int t = 0; t < CASES; t++)
        for (int p = 0; p < K; p++) {
            cases[t][p][0] = next_random() % 50;
            cases[t][p][1] = next_random() % 50;
        }
    long long check = 0;
    for (int r = 0; r < 40; r++)
        for (int t = 0; t < CASES; t++) check = (check * 131 + odd_cells(50, 50, cases[t], K)) % 1000000007;
    printf("40 rounds of 1000 lists of 100 places in 50 by 50: checksum %lld\n", check);
    return 0;
}
