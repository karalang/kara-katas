// LeetCode 794 — Valid Tic-Tac-Toe State: the bench, in C. Mirrors
// valid_tic_tac_toe.kara: count the marks and check the lines.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static const int LINES[8][3] = {{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {2, 4, 6}};

static int wins(const char *cells, char mark) {
    for (int i = 0; i < 8; i++)
        if (cells[LINES[i][0]] == mark && cells[LINES[i][1]] == mark && cells[LINES[i][2]] == mark) return 1;
    return 0;
}

static int valid_tic_tac_toe(char board[3][4]) {
    char cells[9];
    for (int r = 0; r < 3; r++) memcpy(cells + r * 3, board[r], 3);
    int64_t x = 0, o = 0;
    for (int i = 0; i < 9; i++) {
        if (cells[i] == 'X') x++;
        if (cells[i] == 'O') o++;
    }
    if (x != o && x != o + 1) return 0;
    if (wins(cells, 'X') && x != o + 1) return 0;
    if (wins(cells, 'O') && x != o) return 0;
    return 1;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static void random_board(int64_t *seed, char board[3][4]) {
    char cells[9];
    memset(cells, ' ', 9);
    if (next_random(seed) % 2 == 0) {
        const char marks[3] = {' ', 'X', 'O'};
        for (int i = 0; i < 9; i++) cells[i] = marks[next_random(seed) % 3];
    } else {
        int64_t moves = next_random(seed) % 10;
        char mover = 'X';
        for (int64_t m = 0; m < moves; m++) {
            int empty[9], n = 0;
            for (int i = 0; i < 9; i++)
                if (cells[i] == ' ') empty[n++] = i;
            cells[empty[next_random(seed) % n]] = mover;
            mover = mover == 'X' ? 'O' : 'X';
        }
    }
    for (int r = 0; r < 3; r++) {
        memcpy(board[r], cells + r * 3, 3);
        board[r][3] = 0;
    }
}

int main(void) {
    int64_t seed = 794;
    static char boards[4096][3][4];
    for (int k = 0; k < 4096; k++) random_board(&seed, boards[k]);
    int64_t rounds = 6000000, valid = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        if (valid_tic_tac_toe(boards[r % 4096])) {
            valid++;
            check = (check * 131 + r % 4096) % 1000000007;
        }
    }
    printf("%lld boards: %lld valid, checksum %lld\n", (long long)rounds, (long long)valid, (long long)check);
    return 0;
}
