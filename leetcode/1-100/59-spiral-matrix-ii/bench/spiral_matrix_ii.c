// Benchmark workload — Spiral Matrix II (LeetCode #59).
// C mirror of bench/spiral_matrix_ii.kara. Same M=9 rotated sizes (n=12..20),
// K=180k, boundary-shrinking generator, position-weighted checksum, and sink.
// The grid is int64_t** (a row-pointer array + one malloc per row = n+1
// allocations), matching the kara/rust Vec<Vec<i64>> nested-allocation shape
// — apples-to-apples on allocation, not a single flat buffer.

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static int64_t **generate_matrix(int64_t n) {
    int64_t **grid = (int64_t **)malloc(sizeof(int64_t *) * (size_t)n);
    for (int64_t r = 0; r < n; r++) {
        grid[r] = (int64_t *)calloc((size_t)n, sizeof(int64_t));
    }

    int64_t top = 0, bottom = n - 1, left = 0, right = n - 1, v = 1;
    while (top <= bottom && left <= right) {
        for (int64_t c = left; c <= right; c++) {
            grid[top][c] = v++;
        }
        top++;

        for (int64_t r2 = top; r2 <= bottom; r2++) {
            grid[r2][right] = v++;
        }
        right--;

        if (top <= bottom) {
            for (int64_t c2 = right; c2 >= left; c2--) {
                grid[bottom][c2] = v++;
            }
            bottom--;
        }

        if (left <= right) {
            for (int64_t r3 = bottom; r3 >= top; r3--) {
                grid[r3][left] = v++;
            }
            left++;
        }
    }
    return grid;
}

static int64_t checksum(int64_t **grid, int64_t n) {
    int64_t s = 0;
    for (int64_t i = 0; i < n; i++) {
        for (int64_t j = 0; j < n; j++) {
            s += grid[i][j] * (i * n + j + 1);
        }
    }
    return s;
}

static void free_matrix(int64_t **grid, int64_t n) {
    for (int64_t r = 0; r < n; r++) free(grid[r]);
    free(grid);
}

int main(void) {
    const int64_t m_sizes = 9;
    const int64_t k_iters = 180000;

    int64_t total = 0;
    for (int64_t k = 0; k < k_iters; k++) {
        int64_t n = 12 + (k % m_sizes);
        int64_t **g = generate_matrix(n);
        total += checksum(g, n);
        free_matrix(g, n);
    }
    printf("%lld\n", (long long)total);
    return 0;
}
