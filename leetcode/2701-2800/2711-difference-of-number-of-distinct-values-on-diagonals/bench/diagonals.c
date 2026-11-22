// LeetCode #2711: Difference of Number of Distinct Values on Diagonals --
// the bench (diagonals.kara in C): each diagonal swept down and then up
// with a table of the values seen.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define M 50
#define N 50

static void difference_of_distinct_values(const int64_t grid[M][N], int64_t answer[M][N]) {
    for (int s = 0; s < M + N - 1; s++) {
        int r0 = s < N ? 0 : s - N + 1, c0 = s < N ? s : 0;
        int length = (M - r0 < N - c0) ? M - r0 : N - c0;
        bool seen[51];
        memset(seen, 0, sizeof seen);
        int64_t distinct = 0;
        for (int k = 0; k < length; k++) {
            answer[r0 + k][c0 + k] = distinct;
            int64_t v = grid[r0 + k][c0 + k];
            if (!seen[v]) {
                seen[v] = true;
                distinct += 1;
            }
        }
        memset(seen, 0, sizeof seen);
        distinct = 0;
        for (int k = length - 1; k >= 0; k--) {
            int64_t d = answer[r0 + k][c0 + k] - distinct;
            answer[r0 + k][c0 + k] = d < 0 ? -d : d;
            int64_t v = grid[r0 + k][c0 + k];
            if (!seen[v]) {
                seen[v] = true;
                distinct += 1;
            }
        }
    }
}

static int64_t seed = 2711;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int count = 2000, rounds = 5;
    int64_t (*grids)[M][N] = malloc(sizeof(int64_t[M][N]) * count);
    for (int g = 0; g < count; g++) {
        int64_t cap = next_random() % 50 + 1;
        for (int r = 0; r < M; r++)
            for (int c = 0; c < N; c++) grids[g][r][c] = next_random() % cap + 1;
    }
    static int64_t answer[M][N];
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int g = 0; g < count; g++) {
            difference_of_distinct_values(grids[g], answer);
            for (int i = 0; i < M; i++)
                for (int j = 0; j < N; j++) {
                    sum += answer[i][j];
                    check = (check * 31 + answer[i][j]) % 1000000007;
                }
            check = (check + r) % 1000000007;
        }
    }
    printf("%d grids of 50 by 50, %d rounds: differences sum to %lld, checksum %lld\n", count, rounds, (long long)sum, (long long)check);
    free(grids);
    return 0;
}
