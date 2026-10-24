// LeetCode #934: Shortest Bridge -- bench: mark one island, then search
// outward. Mirrors shortest_bridge.kara, .rs, .py and go-seq/. A grid is
// one block of n * n cells, read row by row.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const int64_t DR[4] = {-1, 1, 0, 0};
static const int64_t DC[4] = {0, 0, -1, 1};

static int64_t shortest_bridge(const int64_t *grid, int64_t n) {
    int64_t *dist = malloc(sizeof(int64_t) * (size_t)(n * n));
    int64_t *stack = malloc(sizeof(int64_t) * (size_t)(n * n));
    int64_t *frontier = malloc(sizeof(int64_t) * (size_t)(n * n));
    for (int64_t i = 0; i < n * n; i++) {
        dist[i] = -1;
    }
    int64_t start = 0;
    while (grid[start] == 0) {
        start++;
    }
    int64_t top = 0;
    int64_t len = 0;
    stack[top++] = start;
    dist[start] = 0;
    while (top > 0) {
        int64_t cell = stack[--top];
        frontier[len++] = cell;
        for (int d = 0; d < 4; d++) {
            int64_t r = cell / n + DR[d];
            int64_t c = cell % n + DC[d];
            if (r >= 0 && r < n && c >= 0 && c < n && grid[r * n + c] == 1 && dist[r * n + c] < 0) {
                dist[r * n + c] = 0;
                stack[top++] = r * n + c;
            }
        }
    }
    int64_t answer = -1;
    int64_t head = 0;
    while (head < len && answer < 0) {
        int64_t cell = frontier[head++];
        for (int d = 0; d < 4; d++) {
            int64_t r = cell / n + DR[d];
            int64_t c = cell % n + DC[d];
            if (r >= 0 && r < n && c >= 0 && c < n && dist[r * n + c] < 0) {
                if (grid[r * n + c] == 1) {
                    answer = dist[cell];
                    break;
                }
                dist[r * n + c] = dist[cell] + 1;
                frontier[len++] = r * n + c;
            }
        }
    }
    free(dist);
    free(stack);
    free(frontier);
    return answer;
}

static int64_t seed = 934;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int beside(const int64_t *grid, int64_t n, int64_t r, int64_t c, int64_t mark) {
    return (r > 0 && grid[(r - 1) * n + c] == mark) || (r + 1 < n && grid[(r + 1) * n + c] == mark) ||
           (c > 0 && grid[r * n + c - 1] == mark) || (c + 1 < n && grid[r * n + c + 1] == mark);
}

static void grow(int64_t *grid, int64_t n, int64_t *cells, int64_t *len, int64_t size, int64_t mark,
                 int64_t avoid) {
    int64_t tries = 0;
    while (*len < size && tries < 4 * size) {
        tries++;
        int64_t cell = cells[next_random() % *len];
        int64_t d = next_random() % 4;
        int64_t r = cell / n + DR[d];
        int64_t c = cell % n + DC[d];
        if (r >= 0 && r < n && c >= 0 && c < n && grid[r * n + c] == 0 && !beside(grid, n, r, c, avoid)) {
            grid[r * n + c] = mark;
            cells[(*len)++] = r * n + c;
        }
    }
}

static void random_islands(int64_t *grid, int64_t n, int64_t size_a, int64_t size_b) {
    int64_t *cells = malloc(sizeof(int64_t) * (size_t)(n * n));
    for (;;) {
        memset(grid, 0, sizeof(int64_t) * (size_t)(n * n));
        int64_t a = next_random() % (n * n);
        grid[a] = 2;
        cells[0] = a;
        int64_t len = 1;
        grow(grid, n, cells, &len, size_a, 2, -1);
        int64_t b = -1;
        for (int k = 0; k < 100; k++) {
            int64_t x = next_random() % (n * n);
            if (b < 0 && grid[x] == 0 && !beside(grid, n, x / n, x % n, 2)) {
                b = x;
            }
        }
        if (b >= 0) {
            grid[b] = 3;
            cells[0] = b;
            len = 1;
            grow(grid, n, cells, &len, size_b, 3, 2);
            for (int64_t i = 0; i < n * n; i++) {
                if (grid[i] > 0) {
                    grid[i] = 1;
                }
            }
            free(cells);
            return;
        }
    }
}

int main(void) {
    int64_t rounds = 50;
    int64_t count = 100;
    int64_t n = 100;
    // count n x n grids, each with two islands of up to 2500 cells grown at
    // random, built once
    int64_t *grids = malloc(sizeof(int64_t) * (size_t)(count * n * n));
    for (int64_t g = 0; g < count; g++) {
        int64_t size_a = 1 + next_random() % 2500;
        int64_t size_b = 1 + next_random() % 2500;
        random_islands(grids + g * n * n, n, size_a, size_b);
    }
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        // each round visits every grid, starting from a different one
        for (int64_t i = 0; i < count; i++) {
            int64_t a = shortest_bridge(grids + ((r + i) % count) * n * n, n);
            total += a;
            check = (check * 1000003 + a) % 1000000007;
        }
    }
    printf("%lld rounds over %lld grids of %lld x %lld: answers summing to %lld, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)n, (long long)n, (long long)total,
           (long long)check);
    free(grids);
    return 0;
}
