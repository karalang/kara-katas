#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* The C mirror of ways.kara: the same suffix sums and table, a fresh table
   for each count of pieces, as the Kara arm makes a fresh Vec. */
static int64_t *grid(int rows, int cols) { return calloc((size_t)(rows + 1) * (size_t)(cols + 1), sizeof(int64_t)); }

static int32_t ways(char pizza[50][51], int rows, int cols, int k) {
    int w = cols + 1;
    int64_t *apples = grid(rows, cols);
    for (int r = rows - 1; r >= 0; r--)
        for (int c = cols - 1; c >= 0; c--) {
            int64_t here = pizza[r][c] == 'A';
            apples[r * w + c] = here + apples[(r + 1) * w + c] + apples[r * w + c + 1] - apples[(r + 1) * w + c + 1];
        }
    int64_t *ways = grid(rows, cols);
    for (int r = 0; r < rows; r++)
        for (int c = 0; c < cols; c++)
            if (apples[r * w + c] > 0) ways[r * w + c] = 1;
    for (int p = 1; p < k; p++) {
        int64_t *next = grid(rows, cols);
        for (int r = 0; r < rows; r++)
            for (int c = 0; c < cols; c++) {
                int64_t total = 0;
                for (int cut = r + 1; cut < rows; cut++)
                    if (apples[r * w + c] - apples[cut * w + c] > 0) total += ways[cut * w + c];
                for (int cut = c + 1; cut < cols; cut++)
                    if (apples[r * w + c] - apples[r * w + cut] > 0) total += ways[r * w + cut];
                next[r * w + c] = total % 1000000007;
            }
        free(ways);
        ways = next;
    }
    int32_t got = (int32_t)ways[0];
    free(ways);
    free(apples);
    return got;
}

int main(void) {
    int64_t seed = 1444, check = 0;
    static char pizza[50][51];
    for (int t = 0; t < 200; t++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t rate = 5 + seed / 65536 % 46;
        for (int r = 0; r < 50; r++) {
            for (int c = 0; c < 50; c++) {
                seed = (seed * 1103515245 + 12345) % 2147483648;
                pizza[r][c] = seed / 65536 % 100 < rate ? 'A' : '.';
            }
            pizza[r][50] = 0;
        }
        check = (check * 131 + ways(pizza, 50, 50, 10)) % 1000000007;
    }
    printf("200 pizzas of 50 by 50: checksum %lld\n", (long long)check);
    return 0;
}
