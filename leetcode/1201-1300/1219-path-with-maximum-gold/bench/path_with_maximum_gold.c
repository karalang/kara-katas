// LeetCode #1219 bench, C mirror of the Kāra ★ arm: a depth-first search
// from every cell with gold that zeroes a cell while the search goes on
// from it and puts its gold back on the way out, on 15 by 15 grids each
// holding one blob of 25 cells with gold, grown at random and drawn once.
#include <stdio.h>
#include <stdint.h>

#define N 15
#define GRIDS 160

static int64_t seed = 1219;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t grids[GRIDS][N][N];

static int64_t collect(int64_t g[N][N], int64_t r, int64_t c) {
    if (r < 0 || c < 0 || r >= N || c >= N || g[r][c] == 0) {
        return 0;
    }
    int64_t gold = g[r][c];
    g[r][c] = 0;
    int64_t best = 0;
    static const int64_t dr[4] = {1, -1, 0, 0};
    static const int64_t dc[4] = {0, 0, 1, -1};
    for (int k = 0; k < 4; k++) {
        int64_t v = collect(g, r + dr[k], c + dc[k]);
        if (v > best) best = v;
    }
    g[r][c] = gold;
    return gold + best;
}

static int64_t get_maximum_gold(int64_t g[N][N]) {
    int64_t best = 0;
    for (int64_t r = 0; r < N; r++) {
        for (int64_t c = 0; c < N; c++) {
            if (g[r][c] > 0) {
                int64_t v = collect(g, r, c);
                if (v > best) best = v;
            }
        }
    }
    return best;
}

int main(void) {
    static const int64_t dr[4] = {1, -1, 0, 0};
    static const int64_t dc[4] = {0, 0, 1, -1};
    for (int k = 0; k < GRIDS; k++) {
        int64_t cells[25][2];
        int64_t placed = 1;
        int64_t r0 = next_random() % N, c0 = next_random() % N;
        grids[k][r0][c0] = next_random() % 100 + 1;
        cells[0][0] = r0;
        cells[0][1] = c0;
        while (placed < 25) {
            int64_t at = next_random() % placed;
            int64_t d = next_random() % 4;
            int64_t r = cells[at][0] + dr[d], c = cells[at][1] + dc[d];
            if (r >= 0 && c >= 0 && r < N && c < N && grids[k][r][c] == 0) {
                grids[k][r][c] = next_random() % 100 + 1;
                cells[placed][0] = r;
                cells[placed][1] = c;
                placed++;
            }
        }
    }
    int64_t check = 0, total = 0;
    for (int k = 0; k < GRIDS; k++) {
        int64_t answer = get_maximum_gold(grids[k]);
        total += answer;
        check = (check * 131 + answer) % 1000000007;
    }
    printf("160 grids of 15 by 15, one blob of 25 cells with gold each: gold total %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
