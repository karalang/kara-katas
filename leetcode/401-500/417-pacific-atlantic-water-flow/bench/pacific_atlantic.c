// LeetCode #417: Pacific Atlantic Water Flow -- C mirror of
// pacific_atlantic.kara (search up from each ocean).
// Usage: ./pacific_atlantic [rounds]
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static const int64_t DR[4] = {-1, 1, 0, 0};
static const int64_t DC[4] = {0, 0, -1, 1};

// Returns a fresh grid marking every cell reached uphill from the queued
// cells; the queue holds row * cols + col, from 0 to tail.
static bool *climb(const int64_t *h, int64_t rows, int64_t cols, int64_t *queue, int64_t tail) {
    bool *seen = calloc(rows * cols, sizeof *seen);
    for (int64_t k = 0; k < tail; k++) {
        seen[queue[k]] = true;
    }
    int64_t head = 0;
    while (head < tail) {
        int64_t cell = queue[head++];
        int64_t r = cell / cols, c = cell % cols;
        for (int k = 0; k < 4; k++) {
            int64_t nr = r + DR[k], nc = c + DC[k];
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && !seen[nr * cols + nc] && h[nr * cols + nc] >= h[cell]) {
                seen[nr * cols + nc] = true;
                queue[tail++] = nr * cols + nc;
            }
        }
    }
    return seen;
}

// Returns a fresh array of the answer's cells, row-major, as
// row * cols + col, and sets *count to how many. Like the Kāra program,
// each call allocates its own queues, marks and answer.
static int64_t *pacific_atlantic(const int64_t *h, int64_t rows, int64_t cols, int64_t *count) {
    // A queue holds each cell at most once, plus a corner pushed twice.
    int64_t *queue = malloc((rows * cols + rows + cols) * sizeof *queue);
    int64_t tail = 0;
    for (int64_t r = 0; r < rows; r++) queue[tail++] = r * cols;
    for (int64_t c = 0; c < cols; c++) queue[tail++] = c;
    bool *pac = climb(h, rows, cols, queue, tail);
    tail = 0;
    for (int64_t r = 0; r < rows; r++) queue[tail++] = r * cols + cols - 1;
    for (int64_t c = 0; c < cols; c++) queue[tail++] = (rows - 1) * cols + c;
    bool *atl = climb(h, rows, cols, queue, tail);
    int64_t n = 0;
    for (int64_t k = 0; k < rows * cols; k++) {
        n += pac[k] && atl[k];
    }
    int64_t *cells = malloc((n > 0 ? n : 1) * sizeof *cells);
    n = 0;
    for (int64_t k = 0; k < rows * cols; k++) {
        if (pac[k] && atl[k]) {
            cells[n++] = k;
        }
    }
    free(queue);
    free(pac);
    free(atl);
    *count = n;
    return cells;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t ridge(int64_t r, int64_t c, int64_t n) {
    int64_t a = r + c, b = 2 * n - 2 - r - c;
    return a < b ? a : b;
}

int main(int argc, char **argv) {
    int64_t rounds = argc > 1 ? atoll(argv[1]) : 3000;
    int64_t n = 200, seed = 417;
    int64_t *h = malloc(n * n * sizeof *h);
    for (int64_t r = 0; r < n; r++) {
        for (int64_t c = 0; c < n; c++) {
            h[r * n + c] = 3 * ridge(r, c, n) + step(&seed) % 3;
        }
    }
    int64_t total = 0, checksum = 0;
    for (int64_t k = 0; k < rounds; k++) {
        int64_t r = step(&seed) % n;
        int64_t c = step(&seed) % n;
        h[r * n + c] = step(&seed) % (3 * ridge(r, c, n) + 3);
        int64_t count;
        int64_t *cells = pacific_atlantic(h, n, n, &count);
        total += count;
        int64_t last = cells[count - 1];
        free(cells);
        checksum = (checksum * 31 + count + (last / n) * n + last % n) % 1000000007;
    }
    printf("%lld rounds on a %lldx%lld grid: %lld cells, checksum %lld\n", (long long)rounds, (long long)n, (long long)n, (long long)total, (long long)checksum);
    free(h);
    return 0;
}
