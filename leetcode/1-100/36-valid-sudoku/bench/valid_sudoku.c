/* LeetCode #36 bench — C (mirror of valid_sudoku.kara).
 *
 * Single-pass bitmask validation of a 9x9 board with three stack int64_t[9] mask
 * arrays, perturb-validate-restore TOTAL times with the verdict folded into a
 * checksum. The no-allocation floor: the board and masks are all stack storage,
 * the validator is pure index arithmetic.
 */
#include <stdio.h>
#include <stdint.h>

static int64_t box_index(int64_t r, int64_t c) {
    return (r / 3) * 3 + c / 3;
}

static int is_valid(const int64_t *board) {
    int64_t rows[9] = {0}, cols[9] = {0}, boxes[9] = {0};
    for (int64_t r = 0; r < 9; r++) {
        for (int64_t c = 0; c < 9; c++) {
            int64_t d = board[r * 9 + c];
            if (d != 0) {
                int64_t bit = (int64_t)1 << d;
                int64_t b = box_index(r, c);
                if ((rows[r] & bit) != 0 || (cols[c] & bit) != 0 || (boxes[b] & bit) != 0) {
                    return 0;
                }
                rows[r] |= bit;
                cols[c] |= bit;
                boxes[b] |= bit;
            }
        }
    }
    return 1;
}

int main(void) {
    const int64_t total = 5000000;
    const int64_t modulus = 1000000007;

    int64_t board[81] = {
        5, 3, 4, 6, 7, 8, 9, 1, 2, 6, 7, 2, 1, 9, 5, 3, 4, 8, 1, 9, 8, 3, 4, 2, 5, 6, 7, 8, 5, 9,
        7, 6, 1, 4, 2, 3, 4, 2, 6, 8, 5, 3, 7, 9, 1, 7, 1, 3, 9, 2, 4, 8, 5, 6, 9, 6, 1, 5, 3, 7,
        2, 8, 4, 2, 8, 7, 4, 1, 9, 6, 3, 5, 3, 4, 5, 2, 8, 6, 1, 7, 9,
    };

    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        int64_t pos = k % 81;
        int64_t digit = (k % 9) + 1;
        int64_t save = board[pos];
        board[pos] = digit;
        int64_t v = is_valid(board) ? 1 : 0;
        acc = (acc * 31 + v) % modulus;
        board[pos] = save;
    }

    printf("%lld\n", (long long)acc);
    return 0;
}
