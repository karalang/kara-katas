// LeetCode #2123: Minimum Operations to Remove Adjacent Ones in Matrix --
// the benchmark, the same algorithm as isolated.kara: the ones a bipartite
// graph by the parity of row plus column, the answer a maximum matching
// grown by Kuhn's augmenting paths. Each even one's neighbours are kept
// in a fixed slot of four.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 300

static int adj[N * N][4], deg[N * N];
static int64_t partner[N * N], seen[N * N];

static int try_match(int u, int64_t stamp) {
    for (int i = 0; i < deg[u]; i++) {
        int v = adj[u][i];
        if (seen[v] == stamp) continue;
        seen[v] = stamp;
        if (partner[v] < 0 || try_match((int)partner[v], stamp)) {
            partner[v] = u;
            return 1;
        }
    }
    return 0;
}

static int64_t minimum_operations(int grid[N][N]) {
    static const int steps[4][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    for (int r = 0; r < N; r++) {
        for (int c = 0; c < N; c++) {
            int u = r * N + c;
            deg[u] = 0;
            partner[u] = -1;
            seen[u] = -1;
            if (grid[r][c] == 0 || (r + c) % 2 != 0) continue;
            for (int s = 0; s < 4; s++) {
                int nr = r + steps[s][0], nc = c + steps[s][1];
                if (nr >= 0 && nr < N && nc >= 0 && nc < N && grid[nr][nc] == 1) adj[u][deg[u]++] = nr * N + nc;
            }
        }
    }
    int64_t matched = 0;
    for (int u = 0; u < N * N; u++)
        if (deg[u] > 0 && try_match(u, u)) matched++;
    return matched;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int grids[12][N][N];

int main(void) {
    int64_t seed = 2123;
    for (int g = 0; g < 12; g++) {
        int64_t chance = g % 3 + 1;
        for (int r = 0; r < N; r++)
            for (int c = 0; c < N; c++) grids[g][r][c] = next_random(&seed) % 4 < chance ? 1 : 0;
    }
    int64_t total = 0, check = 0;
    for (int round = 0; round < 10; round++) {
        for (int g = 0; g < 12; g++) {
            int cell = (round * 7919 + g * 104729) % 90000;
            grids[g][cell / N][cell % N] = 1 - grids[g][cell / N][cell % N];
            int64_t got = minimum_operations(grids[g]);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    printf("120 solves: %lld operations, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
