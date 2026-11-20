// LeetCode #1247 bench, in C: the ★ arm (the places that differ counted
// by kind over the two strings side by side) on 2000 random pairs of 1000
// letters built once, each with its own mix of x and y, each asked 20
// times; every answer folded into a checksum.

#include <stdio.h>

#define N 1000
#define PAIRS 2000

static long long seed = 1247;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long minimum_swap(const char *s1, const char *s2) {
    long long x_over_y = 0, y_over_x = 0;
    for (int i = 0; s1[i] && s2[i]; i++) {
        if (s1[i] == 'x' && s2[i] == 'y') x_over_y++;
        else if (s1[i] == 'y' && s2[i] == 'x') y_over_x++;
    }
    if ((x_over_y + y_over_x) % 2 == 1) return -1;
    return x_over_y / 2 + y_over_x / 2 + 2 * (x_over_y % 2);
}

static void random_xy(char *s, int n, long long percent) {
    for (int i = 0; i < n; i++) s[i] = next_random() % 100 < percent ? 'x' : 'y';
    s[n] = 0;
}

static char one[PAIRS][N + 1], two[PAIRS][N + 1];

int main(void) {
    for (int p = 0; p < PAIRS; p++) {
        long long p1 = next_random() % 101;
        long long p2 = next_random() % 101;
        random_xy(one[p], N, p1);
        random_xy(two[p], N, p2);
    }
    long long check = 0;
    for (int r = 0; r < 20; r++)
        for (int p = 0; p < PAIRS; p++) check = (check * 131 + minimum_swap(one[p], two[p]) + 1) % 1000000007;
    printf("20 rounds of 2000 pairs of 1000 letters: checksum %lld\n", check);
    return 0;
}
