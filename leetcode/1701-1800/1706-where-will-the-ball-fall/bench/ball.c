// LeetCode #1706: Where Will the Ball Fall -- the bench's C mirror: the ★
// arm on 1000 random boxes of 100 by 100, all drawn first, each answered
// 100 times.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 1000
#define ROUNDS 100
#define SIDE 100

// each ball followed down a row at a time; `answer` gets n columns
static void find_ball(const int32_t *grid, int64_t m, int64_t n, int32_t *answer) {
    for (int64_t start = 0; start < n; start++) {
        int64_t c = start;
        for (int64_t r = 0; r < m; r++) {
            const int32_t *row = grid + r * n;
            int64_t next = c + row[c];
            if (next < 0 || next >= n || row[next] != row[c]) {
                c = -1;
                break;
            }
            c = next;
        }
        answer[start] = (int32_t)c;
    }
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1706;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int32_t *boxes = malloc((size_t)COUNT * SIDE * SIDE * sizeof *boxes);
    for (int64_t b = 0; b < COUNT; b++) {
        // long runs of one slope: a board turns the other way one time in 20
        for (int64_t r = 0; r < SIDE; r++) {
            int32_t board = 1;
            for (int64_t c = 0; c < SIDE; c++) {
                if (next_random() % 20 == 0) {
                    board = -board;
                }
                boxes[(b * SIDE + r) * SIDE + c] = board;
            }
        }
    }
    int32_t *answer = malloc(SIDE * sizeof *answer);
    int64_t out = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int64_t b = 0; b < COUNT; b++) {
            find_ball(boxes + b * SIDE * SIDE, SIDE, SIDE, answer);
            for (int64_t i = 0; i < SIDE; i++) {
                if (answer[i] >= 0) {
                    out++;
                }
                check = (check * 31 + answer[i] + 2 + r) % 1000000007;
            }
        }
    }
    printf("%d boxes of %d by %d, %d rounds: %lld balls out, checksum %lld\n", COUNT, SIDE, SIDE, ROUNDS, (long long)out, (long long)check);
    free(answer);
    free(boxes);
    return 0;
}
