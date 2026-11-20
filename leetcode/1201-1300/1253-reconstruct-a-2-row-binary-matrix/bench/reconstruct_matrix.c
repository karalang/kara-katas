// LeetCode #1253 bench, in C: the ★ arm (the 2s counted first, then each
// column of 1 giving its 1 to the upper row while it has room, and to the
// lower after) on 20 random cases of 100000 columns built once, each with
// its own share of 2s and half of them with no matrix; each asked 50
// times, every answer folded into a checksum.

#include <stdio.h>
#include <stdlib.h>

#define CASES 20
#define N 100000

static long long seed = 1253;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

// Fills `up` and `low` and returns 2, the rows of the matrix, or returns
// 0 when there is none.
static int reconstruct_matrix(long long upper, long long lower, const long long *colsum, int n, long long **up,
                              long long **low) {
    long long twos = 0, ones = 0;
    for (int i = 0; i < n; i++) twos += colsum[i] == 2;
    for (int i = 0; i < n; i++) ones += colsum[i] == 1;
    if (upper < twos || lower < twos || upper + lower != 2 * twos + ones) return 0;
    *up = calloc(n, sizeof(long long));
    *low = calloc(n, sizeof(long long));
    long long left = upper - twos;
    for (int i = 0; i < n; i++) {
        if (colsum[i] == 2) {
            (*up)[i] = 1;
            (*low)[i] = 1;
        } else if (colsum[i] == 1) {
            if (left > 0) {
                (*up)[i] = 1;
                left--;
            } else {
                (*low)[i] = 1;
            }
        }
    }
    return 2;
}

static long long colsums[CASES][N];
static long long uppers[CASES], lowers[CASES];

int main(void) {
    for (int t = 0; t < CASES; t++) {
        long long twos = next_random() % 101;
        long long upper = 0, lower = 0;
        for (int i = 0; i < N; i++) {
            long long v = next_random() % 100 < twos ? 2 : next_random() % 2;
            colsums[t][i] = v;
            if (v == 2) {
                upper++;
                lower++;
            } else if (v == 1) {
                if (next_random() % 2 == 0) upper++;
                else lower++;
            }
        }
        if (t % 2 == 1) upper++;
        uppers[t] = upper;
        lowers[t] = lower;
    }
    long long check = 0;
    for (int r = 0; r < 50; r++)
        for (int t = 0; t < CASES; t++) {
            long long *up = NULL, *low = NULL;
            int rows = reconstruct_matrix(uppers[t], lowers[t], colsums[t], N, &up, &low);
            long long even = 0;
            if (rows)
                for (int i = 0; i < N; i += 2) even += up[i];
            free(up);
            free(low);
            check = (check * 131 + rows + even) % 1000000007;
        }
    printf("50 rounds of 20 cases of 100000 columns: checksum %lld\n", check);
    return 0;
}
