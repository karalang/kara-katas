// LeetCode #695: Max Area of Island -- bench program, C mirror of the union-find arm.
#include <stdio.h>
#include <stdlib.h>

#define M 50
#define N 50

static long long seed = 695;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int find(int *parent, int x) {
    int root = x;
    while (parent[root] != root) root = parent[root];
    while (parent[x] != root) {
        int next = parent[x];
        parent[x] = root;
        x = next;
    }
    return root;
}

static void join(int *parent, long long *size, int a, int b) {
    int x = find(parent, a), y = find(parent, b);
    if (x == y) return;
    if (size[x] < size[y]) {
        int t = x;
        x = y;
        y = t;
    }
    parent[y] = x;
    size[x] += size[y];
}

static long long max_area_of_island(int grid[M][N]) {
    int *parent = malloc(sizeof(int) * M * N);
    long long *size = malloc(sizeof(long long) * M * N);
    for (int i = 0; i < M * N; i++) {
        parent[i] = i;
        size[i] = 1;
    }
    for (int r = 0; r < M; r++)
        for (int c = 0; c < N; c++) {
            if (!grid[r][c]) continue;
            if (r + 1 < M && grid[r + 1][c]) join(parent, size, r * N + c, (r + 1) * N + c);
            if (c + 1 < N && grid[r][c + 1]) join(parent, size, r * N + c, r * N + c + 1);
        }
    long long best = 0;
    for (int r = 0; r < M; r++)
        for (int c = 0; c < N; c++)
            if (grid[r][c] && find(parent, r * N + c) == r * N + c && size[r * N + c] > best) best = size[r * N + c];
    free(parent);
    free(size);
    return best;
}

int main(void) {
    static int grids[40][M][N];
    for (int g = 0; g < 40; g++) {
        long long percent = 30 + next_random() % 41;
        for (int r = 0; r < M; r++)
            for (int c = 0; c < N; c++) grids[g][r][c] = next_random() % 100 < percent;
    }
    int rounds = 300;
    long long total = 0, checksum = 0;
    for (int k = 0; k < rounds; k++)
        for (int g = 0; g < 40; g++) {
            long long r = max_area_of_island(grids[g]);
            total += r;
            checksum = (checksum * 31 + r) % 1000000007;
        }
    printf("%d rounds of 40 grids of 50 by 50: largest areas sum to %lld, checksum %lld\n", rounds, total, checksum);
    return 0;
}
