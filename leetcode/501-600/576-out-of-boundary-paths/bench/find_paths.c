// Benchmark for #576: C mirror of the ★ arm (the ways forward, move by
// move); see find_paths.kara. A fresh grid of counts, one `calloc`'d row
// at a time, for every move, as the Kāra arm makes one.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t **new_grid(int64_t m, int64_t n) {
    int64_t **g = malloc(m * sizeof(int64_t *));
    for (int64_t r = 0; r < m; r++) {
        g[r] = calloc(n, sizeof(int64_t));
    }
    return g;
}

static void free_grid(int64_t **g, int64_t m) {
    for (int64_t r = 0; r < m; r++) {
        free(g[r]);
    }
    free(g);
}

static int64_t find_paths(int64_t m, int64_t n, int64_t max_move, int64_t start_row, int64_t start_column) {
    const int64_t modulus = 1000000007;
    const int64_t moves[4][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    int64_t **ways = new_grid(m, n);
    ways[start_row][start_column] = 1;
    int64_t out = 0;
    for (int64_t k = 0; k < max_move; k++) {
        int64_t **next = new_grid(m, n);
        for (int64_t r = 0; r < m; r++) {
            for (int64_t c = 0; c < n; c++) {
                int64_t here = ways[r][c];
                if (here == 0) {
                    continue;
                }
                for (int d = 0; d < 4; d++) {
                    int64_t nr = r + moves[d][0];
                    int64_t nc = c + moves[d][1];
                    if (nr < 0 || nr >= m || nc < 0 || nc >= n) {
                        out = (out + here) % modulus;
                    } else {
                        next[nr][nc] = (next[nr][nc] + here) % modulus;
                    }
                }
            }
        }
        free_grid(ways, m);
        ways = next;
    }
    free_grid(ways, m);
    return out;
}

// ---- benchmark --------------------------------------------------------------

static int64_t seed = 576;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t count = 5000;
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t g = 0; g < count; g++) {
        int64_t m = 30 + next_random() % 21;
        int64_t n = 30 + next_random() % 21;
        int64_t max_move = 30 + next_random() % 21;
        int64_t r = next_random() % m;
        int64_t c = next_random() % n;
        int64_t got = find_paths(m, n, max_move, r, c);
        total = (total + got) % 1000000007;
        checksum = (checksum * 31 + got) % 1000000007;
    }
    printf("%lld cases up to 50 by 50 and 50 moves: total %lld, checksum %lld\n",
           (long long)count, (long long)total, (long long)checksum);
    return 0;
}
