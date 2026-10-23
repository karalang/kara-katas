// LeetCode #909: Snakes and Ladders -- bench program, C.
//
// A breadth-first search over the squares, on one 20 x 20 board, LeetCode's
// largest, built once. Each round changes one square, to a snake or ladder
// to a random square or to none, solves the board and folds the answer
// into a checksum.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 20

static int64_t cell(int64_t board[N][N], int64_t n, int64_t square) {
    int64_t row = (square - 1) / n;
    int64_t col = row % 2 == 0 ? (square - 1) % n : n - 1 - (square - 1) % n;
    return board[n - 1 - row][col];
}

static int64_t snakes_and_ladders(int64_t board[N][N], int64_t n) {
    int64_t last = n * n;
    int64_t *moves = malloc(sizeof(int64_t) * (last + 1));
    int64_t *queue = malloc(sizeof(int64_t) * (last + 1));
    for (int64_t i = 0; i <= last; i++) moves[i] = -1;
    int64_t head = 0, tail = 0, answer = -1;
    queue[tail++] = 1;
    moves[1] = 0;
    while (head < tail) {
        int64_t s = queue[head++];
        if (s == last) {
            answer = moves[s];
            break;
        }
        for (int64_t roll = 1; roll < 7; roll++) {
            if (s + roll > last) break;
            int64_t here = cell(board, n, s + roll);
            int64_t next = here == -1 ? s + roll : here;
            if (moves[next] == -1) {
                moves[next] = moves[s] + 1;
                queue[tail++] = next;
            }
        }
    }
    free(moves);
    free(queue);
    return answer;
}

static int64_t seed = 909;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t n = N;
    int64_t last = n * n;
    int64_t rounds = 100000;
    int64_t board[N][N];
    for (int64_t i = 0; i < n; i++)
        for (int64_t j = 0; j < n; j++) board[i][j] = -1;
    int64_t stuck = 0, total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t s = 2 + next_random() % (last - 2);
        int64_t row = (s - 1) / n;
        int64_t col = row % 2 == 0 ? (s - 1) % n : n - 1 - (s - 1) % n;
        board[n - 1 - row][col] = next_random() % 2 == 0 ? -1 : 1 + next_random() % last;
        int64_t got = snakes_and_ladders(board, n);
        if (got == -1)
            stuck++;
        else
            total += got;
        check = (check * 31 + got + 2) % 1000000007;
    }
    printf("%lld rounds on a 20 x 20 board: %lld with the end out of reach, the rest summing to %lld, checksum %lld\n",
           (long long)rounds, (long long)stuck, (long long)total, (long long)check);
    return 0;
}
