// LeetCode #1728: Cat and Mouse II -- the bench (mouse.kara): the game
// solved backwards from its ends, a state lost for the player to move
// once every move from it is counted off.
//
// The grid as rows of chars, each player's moves from each cell listed
// once, and the queue a plain array of states, each pushed at most once.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 200
#define ROUNDS 20
#define SIDE 8
#define CELLS (SIDE * SIDE)
#define MOST_MOVES (1 + 4 * SIDE)

typedef struct {
    int n;
    int to[MOST_MOVES];
} Moves;

static void reach(char marks[SIDE][SIDE + 1], int rows, int cols, int at, int jump, Moves *out) {
    static const int dr[4] = {0, 1, 0, -1}, dc[4] = {1, 0, -1, 0};
    int r = at / cols, c = at % cols;
    out->n = 0;
    out->to[out->n++] = at;
    for (int d = 0; d < 4; d++) {
        for (int k = 1; k <= jump; k++) {
            int nr = r + dr[d] * k, nc = c + dc[d] * k;
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols || marks[nr][nc] == '#') {
                break;
            }
            out->to[out->n++] = nr * cols + nc;
        }
    }
}

static int can_mouse_win(char marks[SIDE][SIDE + 1], int rows, int cols, int cat_jump, int mouse_jump) {
    static Moves mouse_moves[CELLS], cat_moves[CELLS];
    static int result[CELLS * CELLS * 2], left[CELLS * CELLS * 2], queue[CELLS * CELLS * 2];
    int cells = rows * cols;
    int mouse = 0, cat = 0, food = 0;
    int open[CELLS];
    for (int at = 0; at < cells; at++) {
        char ch = marks[at / cols][at % cols];
        if (ch == 'M') {
            mouse = at;
        } else if (ch == 'C') {
            cat = at;
        } else if (ch == 'F') {
            food = at;
        }
        open[at] = ch != '#';
        mouse_moves[at].n = 0;
        cat_moves[at].n = 0;
        if (open[at]) {
            reach(marks, rows, cols, at, mouse_jump, &mouse_moves[at]);
            reach(marks, rows, cols, at, cat_jump, &cat_moves[at]);
        }
    }
#define STATE(m, c, t) (((m) * cells + (c)) * 2 + (t))
    memset(result, 0, sizeof(int) * cells * cells * 2);
    memset(left, 0, sizeof(int) * cells * cells * 2);
    int head = 0, tail = 0;
    for (int m = 0; m < cells; m++) {
        for (int c = 0; c < cells; c++) {
            if (!open[m] || !open[c]) {
                continue;
            }
            left[STATE(m, c, 0)] = mouse_moves[m].n;
            left[STATE(m, c, 1)] = cat_moves[c].n;
            int end = (m == c || c == food) ? 2 : (m == food ? 1 : 0);
            if (end != 0) {
                for (int turn = 0; turn < 2; turn++) {
                    result[STATE(m, c, turn)] = end;
                    queue[tail++] = STATE(m, c, turn);
                }
            }
        }
    }
    while (head < tail) {
        int s = queue[head++];
        int turn = s % 2, m = s / 2 / cells, c = s / 2 % cells;
        int won = result[s];
        if (turn == 0) {
            for (int i = 0; i < cat_moves[c].n; i++) {
                int p = STATE(m, cat_moves[c].to[i], 1);
                if (result[p] != 0) {
                    continue;
                }
                if (won == 2) {
                    result[p] = 2;
                    queue[tail++] = p;
                } else if (--left[p] == 0) {
                    result[p] = 1;
                    queue[tail++] = p;
                }
            }
        } else {
            for (int i = 0; i < mouse_moves[m].n; i++) {
                int p = STATE(mouse_moves[m].to[i], c, 0);
                if (result[p] != 0) {
                    continue;
                }
                if (won == 1) {
                    result[p] = 1;
                    queue[tail++] = p;
                } else if (--left[p] == 0) {
                    result[p] = 2;
                    queue[tail++] = p;
                }
            }
        }
    }
    return result[STATE(mouse, cat, 0)] == 1;
#undef STATE
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    static char grids[COUNT][SIDE][SIDE + 1];
    static int cat_jumps[COUNT], mouse_jumps[COUNT];
    int64_t seed = 1728;
    for (int p = 0; p < COUNT; p++) {
        char marks[CELLS];
        int places[CELLS];
        for (int i = 0; i < CELLS; i++) {
            marks[i] = next_random(&seed) % 4 == 0 ? '#' : '.';
            places[i] = i;
        }
        for (int i = 0; i < 3; i++) {
            int j = i + (int)(next_random(&seed) % (CELLS - i));
            int t = places[i];
            places[i] = places[j];
            places[j] = t;
        }
        marks[places[0]] = 'C';
        marks[places[1]] = 'M';
        marks[places[2]] = 'F';
        for (int r = 0; r < SIDE; r++) {
            memcpy(grids[p][r], marks + r * SIDE, SIDE);
            grids[p][r][SIDE] = '\0';
        }
        cat_jumps[p] = (int)(next_random(&seed) % SIDE + 1);
        mouse_jumps[p] = (int)(next_random(&seed) % SIDE + 1);
    }
    int64_t wins = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int p = 0; p < COUNT; p++) {
            int answer = can_mouse_win(grids[p], SIDE, SIDE, cat_jumps[p], mouse_jumps[p]);
            wins += answer;
            check = (check * 31 + (answer ? 2 : 1) + r) % 1000000007;
        }
    }
    printf("%d grids of %d by %d, %d rounds: the mouse wins %lld, checksum %lld\n", COUNT, SIDE, SIDE, ROUNDS,
           (long long)wins, (long long)check);
    return 0;
}
