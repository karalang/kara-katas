// Benchmark lane for LeetCode 317 — C mirror of bench/shortest_distance.kara.
// Build the grid once (20% obstacles, BUILDINGS buildings on corner-reachable
// empty cells), then PASSES one-BFS-per-building passes, each after relocating
// one building to an empty cell chosen from the checksum (moved back after).
#include <stdio.h>
#include <stdlib.h>

#define ROWS 360
#define COLS 360
#define BUILDINGS 20
#define OBSTACLE_PCT 20
#define PASSES 30
#define MASK 1073741823LL

static long long lcg(long long s) {
    return (s * 1103515245LL + 12345LL) & 0x7fffffffLL;
}

static long long *total, *reach, *seen, *dist, *queue;

static long long shortest_distance(const long long *grid, long long rows, long long cols) {
    long long n = rows * cols;
    for (long long i = 0; i < n; i++) { total[i] = 0; reach[i] = 0; seen[i] = 0; dist[i] = 0; }
    long long b = 0;
    for (long long src = 0; src < n; src++) {
        if (grid[src] != 1) continue;
        b++;
        seen[src] = b;
        dist[src] = 0;
        long long head = 0, tail = 0;
        queue[tail++] = src;
        while (head < tail) {
            long long cell = queue[head++];
            long long r = cell / cols, c = cell % cols, d = dist[cell] + 1;
            long long nb;
            if (r > 0) { nb = cell - cols; if (grid[nb] == 0 && seen[nb] != b) { seen[nb] = b; dist[nb] = d; total[nb] += d; reach[nb]++; queue[tail++] = nb; } }
            if (r < rows - 1) { nb = cell + cols; if (grid[nb] == 0 && seen[nb] != b) { seen[nb] = b; dist[nb] = d; total[nb] += d; reach[nb]++; queue[tail++] = nb; } }
            if (c > 0) { nb = cell - 1; if (grid[nb] == 0 && seen[nb] != b) { seen[nb] = b; dist[nb] = d; total[nb] += d; reach[nb]++; queue[tail++] = nb; } }
            if (c < cols - 1) { nb = cell + 1; if (grid[nb] == 0 && seen[nb] != b) { seen[nb] = b; dist[nb] = d; total[nb] += d; reach[nb]++; queue[tail++] = nb; } }
        }
    }
    long long best = -1;
    for (long long i = 0; i < n; i++) {
        if (grid[i] == 0 && reach[i] == b && (best < 0 || total[i] < best)) best = total[i];
    }
    return best;
}

int main(void) {
    long long n = (long long)ROWS * COLS;
    long long seed = 317;
    long long *grid = malloc(n * sizeof(long long));
    total = malloc(n * sizeof(long long));
    reach = malloc(n * sizeof(long long));
    seen = malloc(n * sizeof(long long));
    dist = malloc(n * sizeof(long long));
    queue = malloc(n * sizeof(long long));
    for (long long i = 0; i < n; i++) {
        seed = lcg(seed);
        grid[i] = ((seed / 65536) % 100 < OBSTACLE_PCT) ? 2 : 0;
    }
    grid[0] = 0;

    char *reachable = calloc(n, 1);
    long long head = 0, tail = 0;
    reachable[0] = 1;
    queue[tail++] = 0;
    while (head < tail) {
        long long cell = queue[head++];
        long long r = cell / COLS, c = cell % COLS;
        if (r > 0 && grid[cell - COLS] != 2 && !reachable[cell - COLS]) { reachable[cell - COLS] = 1; queue[tail++] = cell - COLS; }
        if (r < ROWS - 1 && grid[cell + COLS] != 2 && !reachable[cell + COLS]) { reachable[cell + COLS] = 1; queue[tail++] = cell + COLS; }
        if (c > 0 && grid[cell - 1] != 2 && !reachable[cell - 1]) { reachable[cell - 1] = 1; queue[tail++] = cell - 1; }
        if (c < COLS - 1 && grid[cell + 1] != 2 && !reachable[cell + 1]) { reachable[cell + 1] = 1; queue[tail++] = cell + 1; }
    }

    long long sites[BUILDINGS];
    int placed = 0;
    while (placed < BUILDINGS) {
        seed = lcg(seed);
        long long p = (seed / 256) % n;
        if (grid[p] == 0 && reachable[p]) { grid[p] = 1; sites[placed++] = p; }
    }

    long long checksum = 0;
    for (int pass = 0; pass < PASSES; pass++) {
        long long old = sites[pass % BUILDINGS];
        long long i = checksum % n;
        while (grid[i] != 0) i = (i + 1) % n;
        grid[old] = 0;
        grid[i] = 1;
        long long ans = shortest_distance(grid, ROWS, COLS);
        checksum = (checksum * 31 + ans + 7) & MASK;
        grid[i] = 0;
        grid[old] = 1;
    }
    printf("checksum %lld\n", checksum);
    free(grid); free(total); free(reach); free(seen); free(dist); free(queue); free(reachable);
    return 0;
}
