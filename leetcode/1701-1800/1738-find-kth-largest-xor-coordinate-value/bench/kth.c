// LeetCode #1738: Find Kth Largest XOR Coordinate Value -- the bench
// (kth.kara): a prefix XOR table, then a sort.

#include <stdio.h>
#include <stdlib.h>

static int ascending(const void *x, const void *y) {
    int a = *(const int *)x, b = *(const int *)y;
    return (a > b) - (a < b);
}

static int kth_largest_value(int **matrix, long m, long n, int k) {
    int **prefix = malloc(sizeof(int *) * (m + 1));
    for (long i = 0; i <= m; i++) prefix[i] = calloc(n + 1, sizeof(int));
    int *values = malloc(sizeof(int) * m * n);
    long len = 0;
    for (long i = 0; i < m; i++) {
        for (long j = 0; j < n; j++) {
            prefix[i + 1][j + 1] = prefix[i][j + 1] ^ prefix[i + 1][j] ^ prefix[i][j] ^ matrix[i][j];
            values[len++] = prefix[i + 1][j + 1];
        }
    }
    qsort(values, len, sizeof(int), ascending);
    int answer = values[len - k];
    free(values);
    for (long i = 0; i <= m; i++) free(prefix[i]);
    free(prefix);
    return answer;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

static long wide(long *seed) {
    long hi = next_random(seed);
    return hi * 32768 + next_random(seed);
}

int main(void) {
    int count = 4;
    long rounds = 5, side = 1000, seed = 1738;
    int ***matrices = malloc(sizeof(int **) * count);
    int *ks = malloc(sizeof(int) * count);
    for (int p = 0; p < count; p++) {
        matrices[p] = malloc(sizeof(int *) * side);
        for (long i = 0; i < side; i++) {
            matrices[p][i] = malloc(sizeof(int) * side);
            for (long j = 0; j < side; j++) matrices[p][i][j] = (int)(wide(&seed) % 1000001);
        }
        ks[p] = (int)(wide(&seed) % (side * side) + 1);
    }
    long sum = 0, check = 0;
    for (long r = 0; r < rounds; r++) {
        for (int p = 0; p < count; p++) {
            long answer = kth_largest_value(matrices[p], side, side, ks[p]);
            sum += answer;
            check = (check * 31 + answer + ks[p] + r) % 1000000007;
        }
    }
    for (int p = 0; p < count; p++) {
        for (long i = 0; i < side; i++) free(matrices[p][i]);
        free(matrices[p]);
    }
    free(matrices);
    free(ks);
    printf("%d matrices of %ld by %ld, %ld rounds: answers sum to %ld, checksum %ld\n", count, side, side, rounds, sum, check);
    return 0;
}
