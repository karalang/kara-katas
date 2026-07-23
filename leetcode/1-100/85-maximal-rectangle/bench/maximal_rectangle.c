#include <stdio.h>
#include <stdlib.h>

/* Maximal-rectangle (histogram + monotonic stack) as a scalar compute kernel.
 *
 * Build-once + punch: a large 0/1 matrix is generated once with a deterministic
 * 32-bit LCG (overflow-safe in i64; values from the HIGH bits to dodge the LCG's
 * short-period low bits). Each pass flips one cell (so the optimizer cannot
 * hoist) and recomputes the maximal all-1s rectangle: per row it grows a
 * histogram of column runs, then the largest-rectangle-in-histogram is settled
 * with a monotonic stack of increasing-height indices — a data-dependent
 * push/pop whose width math is loop-carried, so it does NOT vectorize.
 * Sink = sum of the max rectangle area over all passes. */

static long rows_g = 70, cols_g = 70;

static long largest_rect(const long *heights, long n, long *stack) {
    long top = 0; /* stack size */
    long best = 0;
    for (long i = 0; i <= n; i++) {
        long h = (i == n) ? 0 : heights[i];
        while (top > 0 && heights[stack[top - 1]] >= h) {
            long t = stack[top - 1];
            long height = heights[t];
            top--;
            long width = (top == 0) ? i : (i - stack[top - 1] - 1);
            long area = height * width;
            if (area > best) best = area;
        }
        stack[top++] = i;
    }
    return best;
}

static long maximal_rectangle(const long *matrix, long rows, long cols,
                              long *heights, long *stack) {
    for (long c = 0; c < cols; c++) heights[c] = 0;
    long best = 0;
    for (long r = 0; r < rows; r++) {
        long base = r * cols;
        for (long c = 0; c < cols; c++) {
            if (matrix[base + c] == 1) heights[c] += 1;
            else heights[c] = 0;
        }
        long a = largest_rect(heights, cols, stack);
        if (a > best) best = a;
    }
    return best;
}

int main(void) {
    long rows = rows_g, cols = cols_g, passes = 11000;
    long total = rows * cols;
    long *matrix = malloc(total * sizeof(long));
    long state = 12345;
    for (long c = 0; c < total; c++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        matrix[c] = ((state >> 16) % 100 < 62) ? 1 : 0;
    }
    long *heights = malloc(cols * sizeof(long));
    long *stack = malloc((cols + 1) * sizeof(long));
    long sink = 0;
    for (long p = 0; p < passes; p++) {
        long rr = p % rows;
        long cc = (p * 131 + 7) % cols;
        long idx = rr * cols + cc;
        matrix[idx] = 1 - matrix[idx];
        sink += maximal_rectangle(matrix, rows, cols, heights, stack);
    }
    printf("%ld\n", sink);
    free(matrix); free(heights); free(stack);
    return 0;
}
