// Benchmark: LeetCode #959 Regions Cut By Slashes -- the ★ arm, four
// triangles per cell, on grids of 30 by 30, LeetCode's largest. Mirrors
// regions_by_slashes.kara, .rs, .py and go-seq/. The union-find is an
// array on the stack, so a call allocates nothing.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 30
#define COUNT 100

static int64_t find(int64_t *parent, int64_t x) {
    int64_t r = x;
    while (parent[r] != r) r = parent[r];
    while (parent[x] != r) {
        int64_t next = parent[x];
        parent[x] = r;
        x = next;
    }
    return r;
}

static void unite(int64_t *parent, int64_t *sets, int64_t a, int64_t b) {
    int64_t ra = find(parent, a), rb = find(parent, b);
    if (ra != rb) {
        parent[ra] = rb;
        (*sets)--;
    }
}

static int64_t regions_by_slashes(char grid[][N + 1], int64_t n) {
    int64_t parent[4 * N * N];
    for (int64_t i = 0; i < 4 * n * n; i++) parent[i] = i;
    int64_t sets = 4 * n * n;
    for (int64_t r = 0; r < n; r++) {
        for (int64_t c = 0; c < n; c++) {
            // triangles 0 top, 1 right, 2 bottom, 3 left
            int64_t t = 4 * (r * n + c);
            char ch = grid[r][c];
            if (ch == ' ') {
                unite(parent, &sets, t, t + 1);
                unite(parent, &sets, t + 1, t + 2);
                unite(parent, &sets, t + 2, t + 3);
            } else if (ch == '/') {
                unite(parent, &sets, t, t + 3);
                unite(parent, &sets, t + 1, t + 2);
            } else {
                unite(parent, &sets, t, t + 1);
                unite(parent, &sets, t + 2, t + 3);
            }
            if (c + 1 < n) unite(parent, &sets, t + 1, t + 4 + 3);
            if (r + 1 < n) unite(parent, &sets, t + 2, t + 4 * n);
        }
    }
    return sets;
}

static int64_t seed = 959;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char grids[COUNT][N][N + 1];

int main(void) {
    int rounds = 300;
    for (int i = 0; i < COUNT; i++) {
        int64_t blank = i % 10;
        for (int r = 0; r < N; r++) {
            for (int c = 0; c < N; c++) {
                if (next_random() % 10 < blank) grids[i][r][c] = ' ';
                else if (next_random() % 2 == 0) grids[i][r][c] = '/';
                else grids[i][r][c] = '\\';
            }
            grids[i][r][N] = '\0';
        }
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < COUNT; i++) {
            int64_t k = regions_by_slashes(grids[(r + i) % COUNT], N);
            total += k;
            check = (check * 31 + k + i) % 1000000007;
        }
    }
    printf("%d rounds over 100 grids of 30 by 30: %lld regions, checksum %lld\n", rounds,
           (long long)total, (long long)check);
    return 0;
}
