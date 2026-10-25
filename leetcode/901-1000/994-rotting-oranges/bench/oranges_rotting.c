// Benchmark: LeetCode #994 Rotting Oranges -- the ★ arm, a
// breadth-first search from every rotten orange at once, on random grids
// of 10 by 10, LeetCode's largest. Mirrors oranges_rotting.kara, .rs, .py
// and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int64_t r, c, t; } Cell;

typedef struct { Cell *items; int64_t head, len, cap; } Queue;

static void push_back(Queue *q, Cell x) {
    if (q->len == q->cap) {
        q->cap = q->cap ? q->cap * 2 : 4;
        q->items = realloc(q->items, sizeof(Cell) * (size_t)q->cap);
    }
    q->items[q->len++] = x;
}

static int64_t oranges_rotting(int64_t **grid, int64_t m, int64_t n) {
    int64_t **g = malloc(sizeof(int64_t *) * (size_t)m);
    for (int64_t r = 0; r < m; r++) {
        g[r] = malloc(sizeof(int64_t) * (size_t)n);
        memcpy(g[r], grid[r], sizeof(int64_t) * (size_t)n);
    }
    Queue queue = {0};
    int64_t fresh = 0;
    for (int64_t r = 0; r < m; r++) {
        for (int64_t c = 0; c < n; c++) {
            if (g[r][c] == 2) push_back(&queue, (Cell){r, c, 0});
            else if (g[r][c] == 1) fresh++;
        }
    }
    static const int64_t steps[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    int64_t minutes = 0;
    while (queue.head < queue.len) {
        Cell x = queue.items[queue.head++];
        minutes = x.t;
        for (int k = 0; k < 4; k++) {
            int64_t nr = x.r + steps[k][0], nc = x.c + steps[k][1];
            if (nr >= 0 && nr < m && nc >= 0 && nc < n && g[nr][nc] == 1) {
                g[nr][nc] = 2;
                fresh--;
                push_back(&queue, (Cell){nr, nc, x.t + 1});
            }
        }
    }
    free(queue.items);
    for (int64_t r = 0; r < m; r++) free(g[r]);
    free(g);
    return fresh > 0 ? -1 : minutes;
}

static int64_t seed = 994;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t **random_grid(void) {
    int64_t **grid = malloc(sizeof(int64_t *) * 10);
    for (int r = 0; r < 10; r++) {
        grid[r] = malloc(sizeof(int64_t) * 10);
        for (int c = 0; c < 10; c++) {
            int64_t k = next_random() % 32;
            grid[r][c] = k < 3 ? 0 : (k == 3 ? 2 : 1);
        }
    }
    return grid;
}

int main(void) {
    int rounds = 20000;
    int64_t **grids[20];
    for (int i = 0; i < 20; i++) grids[i] = random_grid();
    int64_t stuck = 0, total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < 20; i++) {
            int64_t got = oranges_rotting(grids[(r + i) % 20], 10, 10);
            if (got < 0) stuck++;
            else total += got;
            check = (check * 31 + got + 2) % 1000000007;
        }
    }
    printf("%d rounds over 20 grids of 10 by 10: %lld never rot, %lld minutes, checksum %lld\n", rounds,
           (long long)stuck, (long long)total, (long long)check);
    return 0;
}
