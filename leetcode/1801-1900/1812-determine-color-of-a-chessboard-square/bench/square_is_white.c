// LeetCode #1812: Determine Color of a Chessboard Square -- the bench in C:
// the ★ arm over 3 * 10^7 calls, each of the 64 square names built once and
// drawn from the checksum so far.
#include <stdint.h>
#include <stdio.h>

static int square_is_white(const char *coordinates) {
    int64_t file = coordinates[0] - 'a';
    int64_t rank = coordinates[1] - '1';
    return (file + rank) % 2 == 1;
}

int main(void) {
    char names[64][3];
    int k = 0;
    for (int file = 0; file < 8; file++)
        for (int rank = 1; rank < 9; rank++) {
            names[k][0] = (char)('a' + file);
            names[k][1] = (char)('0' + rank);
            names[k][2] = 0;
            k++;
        }
    int64_t check = 0;
    for (int64_t call = 0; call < 30000000; call++)
        check = (check * 3 + (square_is_white(names[(check + call) % 64]) ? 1 : 2)) % 1000000007;
    printf("30000000 calls: checksum %lld\n", (long long)check);
    return 0;
}
