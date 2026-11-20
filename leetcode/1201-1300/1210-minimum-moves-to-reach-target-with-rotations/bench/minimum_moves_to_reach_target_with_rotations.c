// LeetCode #1210 bench, in C: the ★ arm (a breadth-first search over the
// snake's states, its tail cell and whether it lies flat or upright) on 24
// grids of 100 by 100 drawn once, then 40 rounds over the grids, every
// answer folded into a checksum.

#include <stdio.h>
#include <string.h>

#define N 100
#define GRIDS 24

static long long seed = 1210;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int grids[GRIDS][N][N];

static int is_free(int (*g)[N], int n, int r, int c) {
    return r < n && c < n && g[r][c] == 0;
}

static long long minimum_moves(int (*g)[N], int n) {
    static long long dist[N * N * 2];
    static int qr[N * N * 2], qc[N * N * 2], qu[N * N * 2];
    for (int i = 0; i < n * n * 2; i++) dist[i] = -1;
    int head = 0, tail = 0;
    qr[tail] = 0; qc[tail] = 0; qu[tail] = 0; tail++;
    dist[0] = 0;
    while (head < tail) {
        int r = qr[head], c = qc[head], up = qu[head];
        head++;
        long long d = dist[(r * n + c) * 2 + up];
        if (r == n - 1 && c == n - 2 && up == 0) return d;
        int nr[3], nc[3], nu[3], m = 0;
        if (up == 0) {
            if (is_free(g, n, r, c + 2)) { nr[m] = r; nc[m] = c + 1; nu[m] = 0; m++; }
            if (is_free(g, n, r + 1, c) && is_free(g, n, r + 1, c + 1)) {
                nr[m] = r + 1; nc[m] = c; nu[m] = 0; m++;
                nr[m] = r; nc[m] = c; nu[m] = 1; m++;
            }
        } else {
            if (is_free(g, n, r + 2, c)) { nr[m] = r + 1; nc[m] = c; nu[m] = 1; m++; }
            if (is_free(g, n, r, c + 1) && is_free(g, n, r + 1, c + 1)) {
                nr[m] = r; nc[m] = c + 1; nu[m] = 1; m++;
                nr[m] = r; nc[m] = c; nu[m] = 0; m++;
            }
        }
        for (int i = 0; i < m; i++) {
            int at = (nr[i] * n + nc[i]) * 2 + nu[i];
            if (dist[at] < 0) {
                dist[at] = d + 1;
                qr[tail] = nr[i]; qc[tail] = nc[i]; qu[tail] = nu[i]; tail++;
            }
        }
    }
    return -1;
}

static void random_grid(int (*g)[N], int n, int percent) {
    for (int r = 0; r < n; r++)
        for (int c = 0; c < n; c++) {
            int corner = (r == 0 && c < 2) || (r == n - 1 && c >= n - 2);
            g[r][c] = (!corner && next_random() % 100 < percent) ? 1 : 0;
        }
}

static void open_cell(int (*g)[N], int n, int r, int c) {
    if (r < n && c < n) g[r][c] = 0;
}

static void staircase(int (*g)[N], int n, int s) {
    for (int r = 0; r < n; r++)
        for (int c = 0; c < n; c++) g[r][c] = 1;
    for (int k = 0; k * s < n; k++) {
        int at = k * s;
        for (int c = at; c < at + s + 2; c++) open_cell(g, n, at, c);
        for (int r = at; r < at + s + 2; r++) open_cell(g, n, r, at + s);
        for (int d = 0; d < 4; d++) {
            open_cell(g, n, at + d / 2, at + d % 2);
            open_cell(g, n, at + d / 2, at + s + d % 2);
        }
    }
    for (int i = 0; i < n; i++) {
        open_cell(g, n, n - 1, i);
        open_cell(g, n, n - 2, i);
        open_cell(g, n, i, n - 1);
        open_cell(g, n, i, n - 2);
    }
}

int main(void) {
    for (int i = 0; i < 20; i++) random_grid(grids[i], N, i < 8 ? 5 : i < 16 ? 10 : 14);
    for (int s = 3; s < 7; s++) staircase(grids[20 + s - 3], N, s);
    long long check = 0;
    for (int round = 0; round < 40; round++)
        for (int i = 0; i < GRIDS; i++)
            check = (check * 131 + minimum_moves(grids[i], N) + 2 + round) % 1000000007;
    printf("40 rounds over 24 grids of 100 by 100: checksum %lld\n", check);
    return 0;
}
