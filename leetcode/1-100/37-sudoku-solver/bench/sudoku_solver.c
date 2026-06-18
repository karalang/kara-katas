/* LeetCode #37 bench — C (mirror of sudoku_solver.kara).
 *
 * Bitmask backtracking solver over a flat int64_t[81] board with three stack
 * int64_t[9] mask arrays (rows / cols / boxes); linear cell order, ascending digit
 * order, XOR undo. Workload: TOTAL times copy the "world's hardest sudoku" template,
 * clear cell k%81, solve in place, fold a position-weighted signature of the solved
 * grid into a checksum. The no-allocation floor: board and masks are all stack storage.
 */
#include <stdio.h>
#include <stdint.h>

static int64_t box_index(int64_t r, int64_t c) {
    return (r / 3) * 3 + c / 3;
}

static int go(int64_t *board, int64_t *rows, int64_t *cols, int64_t *boxes, int64_t pos) {
    if (pos == 81) {
        return 1;
    }
    int64_t r = pos / 9;
    int64_t c = pos % 9;
    if (board[pos] != 0) {
        return go(board, rows, cols, boxes, pos + 1);
    }
    int64_t b = box_index(r, c);
    int64_t used = rows[r] | cols[c] | boxes[b];
    for (int64_t d = 1; d <= 9; d++) {
        int64_t bit = (int64_t)1 << d;
        if ((used & bit) == 0) {
            board[pos] = d;
            rows[r] |= bit;
            cols[c] |= bit;
            boxes[b] |= bit;
            if (go(board, rows, cols, boxes, pos + 1)) {
                return 1;
            }
            board[pos] = 0;
            rows[r] ^= bit;
            cols[c] ^= bit;
            boxes[b] ^= bit;
        }
    }
    return 0;
}

static int solve(int64_t *board) {
    int64_t rows[9] = {0}, cols[9] = {0}, boxes[9] = {0};
    for (int64_t i = 0; i < 81; i++) {
        int64_t d = board[i];
        if (d != 0) {
            int64_t r = i / 9, c = i % 9;
            int64_t bit = (int64_t)1 << d;
            rows[r] |= bit;
            cols[c] |= bit;
            boxes[box_index(r, c)] |= bit;
        }
    }
    return go(board, rows, cols, boxes, 0);
}

int main(void) {
    const int64_t total = 500;
    const int64_t modulus = 1000000007;

    const int64_t template[81] = {
        8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 6, 0, 0, 0, 0, 0, 0, 7, 0, 0, 9, 0, 2, 0, 0,
        0, 5, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 4, 5, 7, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0,
        0, 0, 1, 0, 0, 0, 0, 6, 8, 0, 0, 8, 5, 0, 0, 0, 1, 0, 0, 9, 0, 0, 0, 0, 4, 0, 0,
    };

    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        int64_t work[81];
        for (int64_t j = 0; j < 81; j++) {
            work[j] = template[j];
        }
        work[k % 81] = 0;

        solve(work);

        int64_t sig = 0;
        for (int64_t i = 0; i < 81; i++) {
            sig += work[i] * (i + 1);
        }
        acc = (acc * 31 + sig) % modulus;
    }

    printf("%lld\n", (long long)acc);
    return 0;
}
