// LeetCode #2258: Escape the Spreading Fire -- C mirror of the ★ arm:
// fire times by one breadth-first search from every fire, then a binary
// search over the wait, each wait tried by a breadth-first search of the
// person. Same workload and checksum as escape.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NEVER 1000000000000LL

static int64_t seed = 2258;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static const int DR[4] = {-1, 1, 0, 0};
static const int DC[4] = {0, 0, -1, 1};

static int64_t *fire_times(const int8_t *grid, int m, int n, int *queue) {
    int64_t *at = malloc(sizeof(int64_t) * m * n);
    int head = 0, tail = 0;
    for (int i = 0; i < m * n; i++) {
        at[i] = NEVER;
        if (grid[i] == 1) {
            at[i] = 0;
            queue[tail++] = i;
        }
    }
    while (head < tail) {
        int i = queue[head++], r = i / n, c = i % n;
        for (int d = 0; d < 4; d++) {
            int nr = r + DR[d], nc = c + DC[d];
            if (nr >= 0 && nr < m && nc >= 0 && nc < n) {
                int j = nr * n + nc;
                if (grid[j] == 0 && at[j] == NEVER) {
                    at[j] = at[i] + 1;
                    queue[tail++] = j;
                }
            }
        }
    }
    return at;
}

static int escapes(const int8_t *grid, int m, int n, const int64_t *fire, int64_t wait, int *queue, int64_t *when, char *seen) {
    if (wait >= fire[0]) return 0;
    memset(seen, 0, m * n);
    seen[0] = 1;
    when[0] = wait;
    int head = 0, tail = 0, home = m * n - 1;
    queue[tail++] = 0;
    while (head < tail) {
        int i = queue[head++], r = i / n, c = i % n;
        int64_t t = when[i];
        for (int d = 0; d < 4; d++) {
            int nr = r + DR[d], nc = c + DC[d];
            if (nr < 0 || nr >= m || nc < 0 || nc >= n) continue;
            int j = nr * n + nc;
            if (grid[j] != 0 || seen[j]) continue;
            if (j == home) {
                if (t + 1 <= fire[j]) return 1;
                continue;
            }
            if (t + 1 < fire[j]) {
                seen[j] = 1;
                when[j] = t + 1;
                queue[tail++] = j;
            }
        }
    }
    return 0;
}

static int64_t maximum_minutes(const int8_t *grid, int m, int n) {
    int cells = m * n;
    int *queue = malloc(sizeof(int) * cells);
    int64_t *when = malloc(sizeof(int64_t) * cells);
    char *seen = malloc(cells);
    int64_t *fire = fire_times(grid, m, n, queue);
    int64_t result;
    if (!escapes(grid, m, n, fire, 0, queue, when, seen)) {
        result = -1;
    } else if (escapes(grid, m, n, fire, cells, queue, when, seen)) {
        result = 1000000000;
    } else {
        int64_t lo = 0, hi = cells;
        while (hi - lo > 1) {
            int64_t mid = (lo + hi) / 2;
            if (escapes(grid, m, n, fire, mid, queue, when, seen)) lo = mid;
            else hi = mid;
        }
        result = lo;
    }
    free(queue); free(when); free(seen); free(fire);
    return result;
}

static int8_t *chase(int m, int n, int walls) {
    int8_t *grid = malloc(m * n);
    for (int r = 0; r < m; r++)
        for (int c = 0; c < n; c++) {
            int64_t roll = next_random() % 100;
            grid[r * n + c] = (c == 1 && r > 0) ? 2 : (c >= 2 && roll < walls) ? 2 : 0;
        }
    grid[2] = 0;
    grid[m * n - 1] = 0;
    grid[(next_random() % (m - 1) + 1) * n] = 1;
    return grid;
}

int main(void) {
    int shapes[3][2] = {{100, 200}, {200, 100}, {125, 160}};
    int64_t check = 0, waits = 0;
    for (int t = 0; t < 300; t++) {
        int m = shapes[t % 3][0], n = shapes[t % 3][1];
        int8_t *grid = chase(m, n, 8);
        int64_t answer = maximum_minutes(grid, m, n);
        free(grid);
        if (answer >= 0 && answer < 1000000000) waits++;
        check = (check * 31 + answer + 1) % 1000000007;
    }
    printf("300 grids of 2 * 10^4 cells: %lld with a wait, checksum %lld\n", (long long)waits, (long long)check);
    return 0;
}
