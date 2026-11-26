// LeetCode #1460 bench in C: the ★ arm (both arrays sorted and compared)
// on the same 200 pairs of 1000 values and 50 passes.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 1000

static int by_value(const void *x, const void *y) {
    int a = *(const int *)x, b = *(const int *)y;
    return (a > b) - (a < b);
}

static int can_be_equal(const int *target, const int *arr, int n) {
    int *a = malloc(sizeof(int) * n);
    int *b = malloc(sizeof(int) * n);
    memcpy(a, target, sizeof(int) * n);
    memcpy(b, arr, sizeof(int) * n);
    qsort(a, n, sizeof(int), by_value);
    qsort(b, n, sizeof(int), by_value);
    int same = memcmp(a, b, sizeof(int) * n) == 0;
    free(a);
    free(b);
    return same;
}

static int64_t seed = 1460;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int targets[200][N], arrs[200][N];
    for (int p = 0; p < 200; p++) {
        for (int k = 0; k < N; k++) targets[p][k] = (int)(1 + next_random() % 1000);
        memcpy(arrs[p], targets[p], sizeof arrs[p]);
        for (int i = N - 1; i >= 1; i--) {
            int j = (int)(next_random() % (i + 1));
            int t = arrs[p][i];
            arrs[p][i] = arrs[p][j];
            arrs[p][j] = t;
        }
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 50; pass++) {
        for (int p = 0; p < 200; p++) {
            arrs[p][check % N] = targets[p][(check / 7) % N];
            int same = can_be_equal(targets[p], arrs[p], N);
            check = (check * 31 + same + pass) % 1000000007;
        }
    }
    printf("50 passes over 200 pairs of 1000 values: checksum %lld\n", (long long)check);
    return 0;
}
