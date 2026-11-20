// LeetCode #1263 bench, in C: the ★ arm's 0-1 BFS over (box, player)
// states (a step to the front of a ring-buffer deque, a push to the back,
// a state final the first time it leaves) on 100 random 20 by 20 grids, a
// cell in 10 a wall, built once, 20 rounds; every answer folded into a
// checksum. Each state enters the deque at most 4 times, so a ring of
// 2^20 entries never fills.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define RING (1 << 20)

typedef struct { int64_t b, p, pushes; } State;

static int64_t min_push_box(char **grid, int64_t m, int64_t n, State *ring) {
    int64_t player = 0, box_at = 0, target = 0;
    for (int64_t r = 0; r < m; r++)
        for (int64_t c = 0; c < n; c++) {
            char ch = grid[r][c];
            if (ch == 'S') player = r * n + c;
            else if (ch == 'B') box_at = r * n + c;
            else if (ch == 'T') target = r * n + c;
        }
    int64_t cells = m * n;
    bool *done = calloc((size_t)(cells * cells), 1);
    size_t head = 0, len = 0;
    ring[0] = (State){box_at, player, 0};
    len = 1;
    static const int64_t dirs[4][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    int64_t answer = -1;
    while (len > 0) {
        State s = ring[head];
        head = (head + 1) & (RING - 1);
        len--;
        if (done[s.b * cells + s.p]) continue;
        done[s.b * cells + s.p] = true;
        if (s.b == target) { answer = s.pushes; break; }
        for (int d = 0; d < 4; d++) {
            int64_t dr = dirs[d][0], dc = dirs[d][1];
            int64_t r = s.p / n + dr, c = s.p % n + dc;
            if (r < 0 || r >= m || c < 0 || c >= n || grid[r][c] == '#') continue;
            int64_t q = r * n + c;
            if (q != s.b) {
                head = (head - 1) & (RING - 1);
                ring[head] = (State){s.b, q, s.pushes};
                len++;
                continue;
            }
            int64_t br = r + dr, bc = c + dc;
            if (br >= 0 && br < m && bc >= 0 && bc < n && grid[br][bc] != '#') {
                ring[(head + len) & (RING - 1)] = (State){br * n + bc, q, s.pushes + 1};
                len++;
            }
        }
    }
    free(done);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static bool is_mark(char ch) { return ch == 'S' || ch == 'B' || ch == 'T'; }

static char **random_grid(int64_t m, int64_t n, int64_t walls, int64_t *seed) {
    char **grid = malloc(sizeof(char *) * (size_t)m);
    for (int64_t r = 0; r < m; r++) {
        grid[r] = malloc((size_t)n);
        for (int64_t c = 0; c < n; c++) grid[r][c] = next_random(seed) % walls == 0 ? '#' : '.';
    }
    const char marks[3] = {'S', 'B', 'T'};
    for (int k = 0; k < 3; k++) {
        int64_t p = next_random(seed) % (m * n);
        while (is_mark(grid[p / n][p % n])) p = (p + 1) % (m * n);
        grid[p / n][p % n] = marks[k];
    }
    return grid;
}

int main(void) {
    int64_t seed = 1263;
    char **grids[100];
    for (int g = 0; g < 100; g++) grids[g] = random_grid(20, 20, 10, &seed);
    State *ring = malloc(sizeof(State) * RING);
    int64_t check = 0, total = 0;
    for (int64_t round = 0; round < 20; round++)
        for (int g = 0; g < 100; g++) {
            int64_t pushes = min_push_box(grids[g], 20, 20, ring);
            if (pushes > 0) total += pushes;
            check = (check * 131 + pushes + 1 + round) % 1000000007;
        }
    printf("20 rounds of 100 grids of 20 by 20: %lld pushes, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
