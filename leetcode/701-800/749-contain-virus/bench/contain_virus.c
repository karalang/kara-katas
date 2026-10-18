// LeetCode 749 — Contain Virus, bench: the ★ arm (flood fill each day)
// on a 50 x 50 grid that keeps changing. Mirrors contain_virus.kara.
#include <stdint.h>
#include <stdio.h>

#define M 50
#define N 50
#define CELLS (M * N)

static int64_t contain_virus(const int64_t grid[M][N]) {
    int64_t g[CELLS];
    for (int r = 0; r < M; r++)
        for (int c = 0; c < N; c++) g[r * N + c] = grid[r][c];
    static int64_t region[CELLS], mark[CELLS], stack[CELLS];
    // each region's cells and threatened cells, packed one region after
    // another; a region's threatened cells are distinct, so at most CELLS
    static int64_t cells[CELLS], threats[CELLS * 4];
    static int64_t cell_start[CELLS + 1], threat_start[CELLS + 1], needs[CELLS];
    int64_t walls = 0;
    for (;;) {
        for (int i = 0; i < CELLS; i++) region[i] = mark[i] = -1;
        int64_t count = 0, ncells = 0, nthreats = 0;
        for (int64_t start = 0; start < CELLS; start++) {
            if (g[start] != 1 || region[start] != -1) continue;
            int64_t id = count++;
            cell_start[id] = ncells;
            threat_start[id] = nthreats;
            int64_t need = 0, top = 0;
            stack[top++] = start;
            region[start] = id;
            while (top > 0) {
                int64_t at = stack[--top];
                cells[ncells++] = at;
                int64_t r = at / N, c = at % N, next[4], k = 0;
                if (r > 0) next[k++] = at - N;
                if (r < M - 1) next[k++] = at + N;
                if (c > 0) next[k++] = at - 1;
                if (c < N - 1) next[k++] = at + 1;
                for (int64_t j = 0; j < k; j++) {
                    int64_t y = next[j];
                    if (g[y] == 0) {
                        need++;
                        if (mark[y] != id) {
                            mark[y] = id;
                            threats[nthreats++] = y;
                        }
                    } else if (g[y] == 1 && region[y] == -1) {
                        region[y] = id;
                        stack[top++] = y;
                    }
                }
            }
            needs[id] = need;
        }
        cell_start[count] = ncells;
        threat_start[count] = nthreats;
        int64_t best = -1;
        for (int64_t id = 0; id < count; id++) {
            int64_t t = threat_start[id + 1] - threat_start[id];
            if (t > 0 && (best == -1 || t > threat_start[best + 1] - threat_start[best])) best = id;
        }
        if (best == -1) break;
        walls += needs[best];
        for (int64_t id = 0; id < count; id++) {
            if (id == best) {
                for (int64_t k = cell_start[id]; k < cell_start[id + 1]; k++) g[cells[k]] = 2;
            } else {
                for (int64_t k = threat_start[id]; k < threat_start[id + 1]; k++) g[threats[k]] = 1;
            }
        }
    }
    return walls;
}

static int64_t seed = 749;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t rounds = 3000;
    static int64_t grid[M][N];
    for (int r = 0; r < M; r++)
        for (int c = 0; c < N; c++) grid[r][c] = next_random() % 100 < 5 ? 1 : 0;
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int k = 0; k < 20; k++) {
            int64_t r = next_random() % 50;
            int64_t c = next_random() % 50;
            grid[r][c] = next_random() % 100 < 5 ? 1 : 0;
        }
        int64_t w = contain_virus(grid);
        total += w;
        check = (check * 31 + w) % 1000000007;
    }
    printf("%lld grids of 50 x 50: %lld walls in all, checksum %lld\n", (long long)rounds, (long long)total, (long long)check);
    return 0;
}
