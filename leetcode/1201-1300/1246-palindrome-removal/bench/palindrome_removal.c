// LeetCode #1246 bench, in C: the ★ arm (interval dynamic programming,
// rows from the last, one fixed table) on 1000 random arrays of 100
// values built once, each from 1 to v distinct values with v from 1 to 20,
// each asked twice; every answer folded into a checksum.

#include <stdio.h>

#define N 100
#define ARRAYS 1000

static long long seed = 1246;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long best[N + 1][N + 1];

static long long minimum_moves(const long long *arr, int n) {
    for (int i = 0; i <= n; i++) best[i][i] = 0;
    for (int i = n - 1; i >= 0; i--) {
        for (int j = i + 1; j <= n; j++) {
            long long moves = 1 + best[i + 1][j];
            if (i + 1 < j && arr[i + 1] == arr[i] && 1 + best[i + 2][j] < moves) moves = 1 + best[i + 2][j];
            for (int k = i + 2; k < j; k++)
                if (arr[k] == arr[i] && best[i + 1][k] + best[k + 1][j] < moves)
                    moves = best[i + 1][k] + best[k + 1][j];
            best[i][j] = moves;
        }
    }
    return best[0][n];
}

static long long arrays[ARRAYS][N];

int main(void) {
    for (int a = 0; a < ARRAYS; a++) {
        long long values = next_random() % 20 + 1;
        for (int i = 0; i < N; i++) arrays[a][i] = next_random() % values + 1;
    }
    long long check = 0;
    for (int r = 0; r < 2; r++)
        for (int a = 0; a < ARRAYS; a++) check = (check * 131 + minimum_moves(arrays[a], N)) % 1000000007;
    printf("2 rounds of 1000 arrays of 100 values: checksum %lld\n", check);
    return 0;
}
