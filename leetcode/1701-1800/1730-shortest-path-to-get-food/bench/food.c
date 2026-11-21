// LeetCode #1730: Shortest Path to Get Food -- the bench (food.kara): a
// breadth-first search from you, the first food off the queue the
// nearest.
//
// The queue an array of cells, each pushed at most once, where Kāra,
// Rust and Python use a deque of (row, column) pairs.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 10
#define ROUNDS 200
#define SIDE 200

static int32_t get_food(char grid[SIDE][SIDE], int rows, int cols) {
    static int32_t distance[SIDE][SIDE];
    static int queue[SIDE * SIDE];
    static const int dr[4] = {-1, 1, 0, 0}, dc[4] = {0, 0, -1, 1};
    int head = 0, tail = 0;
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            distance[r][c] = -1;
            if (grid[r][c] == '*') {
                distance[r][c] = 0;
                queue[tail++] = r * cols + c;
            }
        }
    }
    while (head < tail) {
        int at = queue[head++];
        int r = at / cols, c = at % cols;
        if (grid[r][c] == '#') {
            return distance[r][c];
        }
        for (int d = 0; d < 4; d++) {
            int nr = r + dr[d], nc = c + dc[d];
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) {
                continue;
            }
            if (grid[nr][nc] != 'X' && distance[nr][nc] < 0) {
                distance[nr][nc] = distance[r][c] + 1;
                queue[tail++] = nr * cols + nc;
            }
        }
    }
    return -1;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t wide(int64_t *seed) {
    int64_t a = next_random(seed);
    return a * 32768 + next_random(seed);
}

int main(void) {
    static char problems[COUNT][SIDE][SIDE];
    int64_t seed = 1730;
    for (int p = 0; p < COUNT; p++) {
        for (int r = 0; r < SIDE; r++) {
            for (int c = 0; c < SIDE; c++) {
                int64_t x = next_random(&seed) % 20000;
                problems[p][r][c] = x < 5000 ? 'X' : (x < 5001 ? '#' : 'O');
            }
        }
        int64_t at = wide(&seed) % (SIDE * SIDE);
        problems[p][at / SIDE][at % SIDE] = '*';
    }
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int p = 0; p < COUNT; p++) {
            int64_t answer = get_food(problems[p], SIDE, SIDE);
            sum += answer;
            check = (check * 31 + answer + 1 + r) % 1000000007;
        }
    }
    printf("%d grids of %d by %d, %d rounds: answers sum to %lld, checksum %lld\n", COUNT, SIDE, SIDE, ROUNDS,
           (long long)sum, (long long)check);
    return 0;
}
