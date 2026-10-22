// LeetCode #864: Shortest Path to Get All Keys -- C mirror of the bench
// program (the ★ arm, breadth-first search over (cell, keys held) states).
// The queue is an array with a head and a tail, since every state enters
// it at most once.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ROWS 30
#define COLS 30

static int64_t shortest_path_all_keys(char grid[][COLS + 1], int64_t rows, int64_t cols) {
    int64_t size = rows * cols;
    char *cells = malloc(size);
    for (int64_t r = 0; r < rows; r++) {
        memcpy(cells + r * cols, grid[r], cols);
    }
    int64_t start = 0, keys = 0;
    for (int64_t i = 0; i < size; i++) {
        if (cells[i] == '@') {
            start = i;
        } else if (cells[i] >= 'a' && cells[i] <= 'f') {
            keys++;
        }
    }
    int64_t all = (1 << keys) - 1;
    int64_t states = size << keys;
    char *seen = calloc(states, 1);
    int64_t *qcell = malloc(states * sizeof(int64_t));
    int64_t *qheld = malloc(states * sizeof(int64_t));
    int64_t *qsteps = malloc(states * sizeof(int64_t));
    int64_t head = 0, tail = 0, answer = -1;
    seen[start] = 1;
    qcell[tail] = start;
    qheld[tail] = 0;
    qsteps[tail++] = 0;
    static const int64_t dr[4] = {-1, 1, 0, 0}, dc[4] = {0, 0, -1, 1};
    while (head < tail) {
        int64_t cell = qcell[head], held = qheld[head], steps = qsteps[head];
        head++;
        if (held == all) {
            answer = steps;
            break;
        }
        int64_t r = cell / cols, c = cell % cols;
        for (int d = 0; d < 4; d++) {
            int64_t nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) {
                continue;
            }
            int64_t next = nr * cols + nc;
            char b = cells[next];
            if (b == '#') {
                continue;
            }
            if (b >= 'A' && b <= 'F' && (held & (1 << (b - 'A'))) == 0) {
                continue;
            }
            int64_t now = held;
            if (b >= 'a' && b <= 'f') {
                now = held | (1 << (b - 'a'));
            }
            if (!seen[now * size + next]) {
                seen[now * size + next] = 1;
                qcell[tail] = next;
                qheld[tail] = now;
                qsteps[tail++] = steps + 1;
            }
        }
    }
    free(cells);
    free(seen);
    free(qcell);
    free(qheld);
    free(qsteps);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t rows = ROWS, cols = COLS, rounds = 1000, seed = 864;
    char cells[ROWS * COLS];
    for (int64_t i = 0; i < rows * cols; i++) {
        cells[i] = next_random(&seed) % 100 < 20 ? '#' : '.';
    }
    for (int i = 0; i < 12; i++) {
        int64_t at = next_random(&seed) % (rows * cols);
        while (cells[at] != '.') {
            at = next_random(&seed) % (rows * cols);
        }
        cells[at] = i < 6 ? 'a' + i : 'A' + i - 6;
    }
    int64_t reached = 0, total = 0, check = 0;
    char grid[ROWS][COLS + 1];
    for (int64_t k = 0; k < rounds; k++) {
        int64_t start = next_random(&seed) % (rows * cols);
        while (cells[start] != '.') {
            start = next_random(&seed) % (rows * cols);
        }
        cells[start] = '@';
        for (int64_t r = 0; r < rows; r++) {
            memcpy(grid[r], cells + r * cols, cols);
            grid[r][cols] = 0;
        }
        cells[start] = '.';
        int64_t moves = shortest_path_all_keys(grid, rows, cols);
        if (moves >= 0) {
            reached++;
            total += moves;
        }
        check = (check * 31 + moves + 2) % 1000000007;
    }
    printf("%lld starts on a 30 by 30 grid: %lld reach every key, moves sum to %lld, checksum %lld\n",
           (long long)rounds, (long long)reached, (long long)total, (long long)check);
    return 0;
}
