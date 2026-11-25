// LeetCode #1368 bench -- C: a 0-1 breadth-first search over the cells, a
// step the sign points to costing 0 and going to the front of the deque,
// any other costing 1 and going to its back.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define SIDE 100
#define CELLS (SIDE * SIDE)

static const int MOVES[4][2] = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

// a ring buffer deque of cell indices; a cell can be queued once per
// lowering of its cost, so it grows as needed
static int32_t *ring;
static size_t cap, head, len;

static void grow(void) {
    int32_t *bigger = malloc(sizeof *bigger * cap * 2);
    for (size_t i = 0; i < len; i++) bigger[i] = ring[(head + i) % cap];
    free(ring);
    ring = bigger;
    head = 0;
    cap *= 2;
}

static void push_front(int32_t x) {
    if (len == cap) grow();
    head = (head + cap - 1) % cap;
    ring[head] = x;
    len++;
}

static void push_back(int32_t x) {
    if (len == cap) grow();
    ring[(head + len) % cap] = x;
    len++;
}

static int32_t pop_front(void) {
    int32_t x = ring[head];
    head = (head + 1) % cap;
    len--;
    return x;
}

static int32_t min_cost(int32_t grid[SIDE][SIDE], int m, int n) {
    static int32_t cost[SIDE][SIDE];
    for (int r = 0; r < m; r++)
        for (int c = 0; c < n; c++) cost[r][c] = INT32_MAX;
    head = len = 0;
    cost[0][0] = 0;
    push_back(0);
    while (len > 0) {
        int32_t at = pop_front();
        int r = at / n, c = at % n;
        for (int d = 0; d < 4; d++) {
            int nr = r + MOVES[d][0], nc = c + MOVES[d][1];
            if (nr < 0 || nr >= m || nc < 0 || nc >= n) continue;
            int32_t step = grid[r][c] == d + 1 ? 0 : 1;
            if (cost[r][c] + step < cost[nr][nc]) {
                cost[nr][nc] = cost[r][c] + step;
                if (step == 0) {
                    push_front(nr * n + nc);
                } else {
                    push_back(nr * n + nc);
                }
            }
        }
    }
    return cost[m - 1][n - 1];
}

static int64_t seed = 1368;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int32_t grids[20][SIDE][SIDE];

int main(void) {
    // 20 grids of 100 by 100 signs, the constraints' most, built once;
    // then 600 rounds, each changing one cell's sign and finding the
    // cheapest valid path through that grid, all drawn from the checksum
    // so far
    cap = 1024;
    ring = malloc(sizeof *ring * cap);
    for (int g = 0; g < 20; g++)
        for (int r = 0; r < SIDE; r++)
            for (int c = 0; c < SIDE; c++) grids[g][r][c] = (int32_t)(1 + next_random() % 4);
    int64_t check = 0;
    for (int64_t r = 0; r < 600; r++) {
        int64_t g = check % 20;
        int64_t cell = (check / 20) % CELLS;
        grids[g][cell / SIDE][cell % SIDE] = (int32_t)(1 + (check / 200000) % 4);
        int64_t cost = min_cost(grids[g], SIDE, SIDE);
        check = (check * 31 + cost + r) % 1000000007;
    }
    printf("600 rounds over 20 grids of 100 by 100: checksum %lld\n", (long long)check);
    free(ring);
    return 0;
}
