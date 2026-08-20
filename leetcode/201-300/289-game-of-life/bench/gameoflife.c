/* Benchmark twin for LeetCode #289 — same algorithm as gameoflife.kara.
 *
 * The two-bit in-place encoding: bit 0 is the old generation and is never
 * written during the sweep, bit 1 is the new one. `& 1` on every neighbour read
 * is what makes the sweep order irrelevant.
 */
#include <stdio.h>
#include <stdint.h>

#define ROWS 256
#define COLS 256
#define GENS 60

static int64_t board[ROWS][COLS];

static int64_t next_rand(int64_t s) { return (s * 1103515245 + 12345) & 2147483647; }

static int64_t live_neighbours(int r, int c) {
    int64_t n = 0;
    for (int dr = -1; dr <= 1; dr++)
        for (int dc = -1; dc <= 1; dc++) {
            if (dr == 0 && dc == 0) continue;
            int rr = r + dr, cc = c + dc;
            if (rr >= 0 && rr < ROWS && cc >= 0 && cc < COLS) n += board[rr][cc] & 1;
        }
    return n;
}

static void step(void) {
    for (int r = 0; r < ROWS; r++)
        for (int c = 0; c < COLS; c++) {
            int64_t n = live_neighbours(r, c);
            int alive = (board[r][c] & 1) == 1;
            int lives = alive ? (n == 2 || n == 3) : (n == 3);
            if (lives) board[r][c] |= 2;
        }
    for (int r = 0; r < ROWS; r++)
        for (int c = 0; c < COLS; c++) board[r][c] >>= 1;
}

int main(void) {
    int64_t seed = 20260820;
    for (int r = 0; r < ROWS; r++)
        for (int c = 0; c < COLS; c++) {
            seed = next_rand(seed);
            board[r][c] = ((seed / 65536) % 100) < 35 ? 1 : 0;
        }
    for (int g = 0; g < GENS; g++) step();

    int64_t pop = 0, hash = 0;
    for (int r = 0; r < ROWS; r++)
        for (int c = 0; c < COLS; c++)
            if (board[r][c] == 1) {
                pop++;
                hash = (hash * 31 + ((int64_t)r * COLS + c)) % 1000000007;
            }
    printf("pop %lld hash %lld\n", (long long)pop, (long long)hash);
    return 0;
}
