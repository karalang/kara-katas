// LeetCode #2337: Move Pieces to Obtain a String -- the bench, the ★ arm
// in C: two indices walking the start and the target together, each
// skipping blanks, the pieces matched in order and each `L` no later in
// the target, each `R` no earlier.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define N 100000

static bool can_change(const char *a, const char *b, int64_t n) {
    int64_t i = 0, j = 0;
    for (;;) {
        while (i < n && a[i] == '_') i++;
        while (j < n && b[j] == '_') j++;
        if (i == n || j == n) return i == n && j == n;
        if (a[i] != b[j]) return false;
        if (a[i] == 'L' && i < j) return false;
        if (a[i] == 'R' && i > j) return false;
        i++;
        j++;
    }
}

static int64_t scrambled(int64_t index) { return index * 2654435761LL % 2147483647LL; }

int main(void) {
    static char starts[10][N], targets[10][N];
    for (int64_t q = 0; q < 10; q++) {
        char *cells = targets[q];
        for (int64_t i = 0; i < N; i++) {
            int64_t r = scrambled(q * 100000 + i) % 4;
            cells[i] = r == 0 ? 'L' : r == 1 ? 'R' : '_';
        }
        memcpy(starts[q], cells, N);
        for (int round = 0; round < 3; round++) {
            for (int64_t i = 1; i < N; i++)
                if (cells[i] == 'L' && cells[i - 1] == '_') {
                    cells[i - 1] = 'L';
                    cells[i] = '_';
                }
            for (int64_t i = N - 2; i >= 0; i--)
                if (cells[i] == 'R' && cells[i + 1] == '_') {
                    cells[i + 1] = 'R';
                    cells[i] = '_';
                }
        }
        if (q % 2 == 1) {
            int64_t first = 0;
            while (cells[first] == '_') first++;
            cells[first] = cells[first] == 'L' ? 'R' : 'L';
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 10; p++)
        for (int q = 0; q < 10; q++) {
            bool can = can_change(starts[q], targets[q], N);
            check = (check * 31 + (can ? 2 : 1) + p) % 1000000007;
        }
    printf("10 passes over 10 pairs of 10^5 places: checksum %lld\n", (long long)check);
    return 0;
}
