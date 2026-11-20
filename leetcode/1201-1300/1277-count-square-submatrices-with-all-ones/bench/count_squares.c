// LeetCode #1277 bench, in C: the ★ arm (dynamic programming over the
// sides of the largest squares) on 40 random 300-by-300 matrices, half,
// four fifths, nineteen twentieths and 99 in 100 ones, drawn once; 50
// rounds, every count folded into a checksum. Rows are separately
// allocated, as LeetCode's C signature hands them over.
#include <stdio.h>
#include <stdlib.h>

static long long min3(long long a, long long b, long long c) {
    long long m = a < b ? a : b;
    return m < c ? m : c;
}

static long long count_squares(long long **matrix, int m, int n) {
    long long **side = malloc(m * sizeof(long long *));
    for (int i = 0; i < m; i++) side[i] = calloc(n, sizeof(long long));
    long long total = 0;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            if (matrix[i][j] == 1) {
                side[i][j] = (i == 0 || j == 0) ? 1 : min3(side[i - 1][j], side[i][j - 1], side[i - 1][j - 1]) + 1;
                total += side[i][j];
            }
    for (int i = 0; i < m; i++) free(side[i]);
    free(side);
    return total;
}

static long long seed = 1277;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    long long percents[4] = {50, 80, 95, 99};
    long long **matrices[40];
    for (int k = 0; k < 40; k++) {
        matrices[k] = malloc(300 * sizeof(long long *));
        for (int i = 0; i < 300; i++) {
            matrices[k][i] = malloc(300 * sizeof(long long));
            for (int j = 0; j < 300; j++) matrices[k][i][j] = next_random() % 100 < percents[k % 4] ? 1 : 0;
        }
    }
    long long check = 0;
    for (long long round = 0; round < 50; round++)
        for (int k = 0; k < 40; k++)
            check = (check * 131 + count_squares(matrices[k], 300, 300) + round) % 1000000007;
    printf("50 rounds of 40 matrices of 300 by 300: checksum %lld\n", check);
    return 0;
}
