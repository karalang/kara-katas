// LeetCode #1275 bench, in C: the ★ arm (line sums) asked about every
// position of every game of tic-tac-toe, 549,945 of them, each game carried
// on while the answer is "Pending"; 40 rounds, every answer folded into a
// checksum. The moves are a fixed array of nine pairs and the answer a
// static string.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char *tictactoe(long long moves[][2], int n) {
    long long rows[3] = {0, 0, 0}, cols[3] = {0, 0, 0};
    long long diagonal = 0, anti = 0, turn = 1;
    for (int i = 0; i < n; i++) {
        long long r = moves[i][0], c = moves[i][1];
        rows[r] += turn;
        cols[c] += turn;
        if (r == c) diagonal += turn;
        if (r + c == 2) anti += turn;
        if (llabs(rows[r]) == 3 || llabs(cols[c]) == 3 || llabs(diagonal) == 3 || llabs(anti) == 3)
            return turn == 1 ? "A" : "B";
        turn = -turn;
    }
    return n == 9 ? "Draw" : "Pending";
}

static void walk(long long moves[][2], int *n, long long *check) {
    for (long long square = 0; square < 9; square++) {
        long long r = square / 3, c = square % 3;
        int taken = 0;
        for (int i = 0; i < *n; i++)
            if (moves[i][0] == r && moves[i][1] == c) { taken = 1; break; }
        if (taken) continue;
        moves[*n][0] = r;
        moves[*n][1] = c;
        (*n)++;
        const char *answer = tictactoe(moves, *n);
        long long k = strcmp(answer, "A") == 0 ? 0 : strcmp(answer, "B") == 0 ? 1 : strcmp(answer, "Draw") == 0 ? 2 : 3;
        *check = (*check * 7 + k) % 1000000007;
        if (k == 3) walk(moves, n, check);
        (*n)--;
    }
}

int main(void) {
    long long check = 0;
    for (long long round = 0; round < 40; round++) {
        long long moves[9][2];
        int n = 0;
        walk(moves, &n, &check);
        check = (check * 131 + round) % 1000000007;
    }
    printf("40 rounds of every game: checksum %lld\n", check);
    return 0;
}
