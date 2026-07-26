/* Benchmark harness for LeetCode #240 — Search a 2D Matrix II.
 * Mirrors search_matrix.kara algorithm-for-algorithm.
 */

#include <stdio.h>
#include <stdlib.h>

#define ROWS 1000
#define COLS 1000
#define ITERS 120000

static int search_matrix(const long long *flat, long long rows, long long cols, long long target) {
    if (rows == 0 || cols == 0) {
        return 0;
    }
    long long r = 0;
    long long c = cols - 1;
    while (r < rows && c >= 0) {
        long long v = flat[r * cols + c];
        if (v == target) {
            return 1;
        } else if (v > target) {
            c--;
        } else {
            r++;
        }
    }
    return 0;
}

int main(void) {
    long long *flat = malloc(sizeof(long long) * (size_t)ROWS * COLS);
    for (long long r = 0; r < ROWS; r++) {
        for (long long c = 0; c < COLS; c++) {
            flat[r * COLS + c] = r * 3 + c * 5;
        }
    }
    long long maxv = (ROWS - 1) * 3 + (COLS - 1) * 5;

    long long sink = 0;
    long long x = 12345;
    for (long long it = 0; it < ITERS; it++) {
        x = (x * 1103515245 + 12345) % 2147483648LL;
        long long target = (x / 65536) % (maxv + 2);
        if (search_matrix(flat, ROWS, COLS, target)) {
            sink = (sink + it + 1) % 1000000007LL;
        }
    }
    printf("%lld\n", sink);
    free(flat);
    return 0;
}
