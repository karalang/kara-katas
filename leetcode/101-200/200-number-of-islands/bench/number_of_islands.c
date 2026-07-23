#include <stdio.h>
#include <stdlib.h>

static long num_islands(long *grid, long rows, long cols, long *stack) {
    long count = 0;
    for (long r = 0; r < rows; r++) {
        for (long c = 0; c < cols; c++) {
            if (grid[r * cols + c] == 1) {
                count++;
                long top = 0;
                stack[top++] = r * cols + c;
                grid[r * cols + c] = 0;
                while (top > 0) {
                    long idx = stack[--top];
                    long cr = idx / cols;
                    long cc = idx % cols;
                    if (cr > 0 && grid[(cr - 1) * cols + cc] == 1) {
                        grid[(cr - 1) * cols + cc] = 0;
                        stack[top++] = (cr - 1) * cols + cc;
                    }
                    if (cr + 1 < rows && grid[(cr + 1) * cols + cc] == 1) {
                        grid[(cr + 1) * cols + cc] = 0;
                        stack[top++] = (cr + 1) * cols + cc;
                    }
                    if (cc > 0 && grid[cr * cols + (cc - 1)] == 1) {
                        grid[cr * cols + (cc - 1)] = 0;
                        stack[top++] = cr * cols + (cc - 1);
                    }
                    if (cc + 1 < cols && grid[cr * cols + (cc + 1)] == 1) {
                        grid[cr * cols + (cc + 1)] = 0;
                        stack[top++] = cr * cols + (cc + 1);
                    }
                }
            }
        }
    }
    return count;
}

int main(void) {
    long rows = 80;
    long cols = 80;
    long passes = 13000;
    long total = rows * cols;

    long *master = malloc((size_t)total * sizeof(long));
    long state = 12345;
    for (long g = 0; g < total; g++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        master[g] = ((state >> 16) % 100 < 45) ? 1 : 0;
    }

    long *work = malloc((size_t)total * sizeof(long));
    long *stack = malloc((size_t)total * sizeof(long));
    long sink = 0;
    for (long p = 0; p < passes; p++) {
        state = (state * 1103515245 + 12345) & 2147483647;
        long idx = state % total;
        master[idx] = 1 - master[idx];
        for (long i = 0; i < total; i++) {
            work[i] = master[i];
        }
        sink += num_islands(work, rows, cols, stack);
    }
    printf("%ld\n", sink);
    free(master);
    free(work);
    free(stack);
    return 0;
}
