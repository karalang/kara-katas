// LeetCode #1349 bench -- C: each row's students as a bit mask, best[mask]
// the most students so far with the last row seated as mask.
#include <stdio.h>

static char rooms[20][8][8];

static int max_students(char seats[8][8], int m, int n) {
    int full = 1 << n;
    int best[256], next[256];
    for (int s = 0; s < full; s++) best[s] = -1;
    best[0] = 0;
    for (int i = 0; i < m; i++) {
        int good = 0;
        for (int j = 0; j < n; j++)
            if (seats[i][j] == '.') good |= 1 << j;
        for (int s = 0; s < full; s++) next[s] = -1;
        for (int mask = 0; mask < full; mask++) {
            if ((mask & good) != mask || (mask & (mask << 1)) != 0) continue;
            int here = __builtin_popcount(mask);
            for (int prev = 0; prev < full; prev++) {
                if (best[prev] < 0 || (mask & (prev << 1)) != 0 || (mask & (prev >> 1)) != 0) continue;
                if (best[prev] + here > next[mask]) next[mask] = best[prev] + here;
            }
        }
        for (int s = 0; s < full; s++) best[s] = next[s];
    }
    int top = best[0];
    for (int s = 1; s < full; s++)
        if (best[s] > top) top = best[s];
    return top;
}

int main(void) {
    long long seed = 1349;
    for (int k = 0; k < 20; k++)
        for (int i = 0; i < 8; i++)
            for (int j = 0; j < 8; j++) {
                seed = (seed * 1103515245 + 12345) % 2147483648LL;
                rooms[k][i][j] = (seed / 65536) % 4 == 0 ? '#' : '.';
            }
    long long check = 0;
    for (long long r = 0; r < 3000; r++) {
        int k = check % 20, i = (check / 20) % 8, j = (check / 160) % 8;
        rooms[k][i][j] = rooms[k][i][j] == '.' ? '#' : '.';
        check = (check * 31 + max_students(rooms[k], 8, 8) + r) % 1000000007;
    }
    printf("3000 rounds over 20 rooms of 8 by 8: checksum %lld\n", check);
    return 0;
}
