// benchmark's C mirror of cells.kara (LeetCode #2194, the ★ arm): two
// loops over the range's bytes, each cell a malloc'd two-letter string.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char **cells_in_range(const char *s, long long *count) {
    long long n = (s[3] - s[0] + 1) * (s[4] - s[1] + 1);
    char **cells = malloc(sizeof(char *) * n);
    long long k = 0;
    for (char col = s[0]; col <= s[3]; col++) {
        for (char row = s[1]; row <= s[4]; row++) {
            char *cell = malloc(3);
            cell[0] = col;
            cell[1] = row;
            cell[2] = 0;
            cells[k++] = cell;
        }
    }
    *count = n;
    return cells;
}

int main(void) {
    const char *letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    static char ranges[15795][6];
    int nr = 0;
    for (int c1 = 0; c1 < 26; c1++)
        for (int c2 = c1; c2 < 26; c2++)
            for (int r1 = 1; r1 < 10; r1++)
                for (int r2 = r1; r2 < 10; r2++) {
                    ranges[nr][0] = letters[c1];
                    ranges[nr][1] = (char)('0' + r1);
                    ranges[nr][2] = ':';
                    ranges[nr][3] = letters[c2];
                    ranges[nr][4] = (char)('0' + r2);
                    ranges[nr][5] = 0;
                    nr++;
                }
    long long check = 0;
    for (int p = 0; p < 20; p++) {
        for (int i = 0; i < nr; i++) {
            long long n;
            char **cells = cells_in_range(ranges[i], &n);
            const char *last = cells[n - 1];
            check = (check * 31 + n * 1000 + last[0] * 10 + last[1]) % 1000000007;
            for (long long k = 0; k < n; k++) free(cells[k]);
            free(cells);
        }
    }
    printf("20 passes over %d ranges: checksum %lld\n", nr, check);
    return 0;
}
