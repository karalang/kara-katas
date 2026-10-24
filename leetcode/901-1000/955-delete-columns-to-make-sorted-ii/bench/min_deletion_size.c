// LeetCode #955: Delete Columns to Make Sorted II -- C mirror of the Kara
// bench program (pairs settled).
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long min_deletion_size(char **strs, long n, long m) {
    bool *settled = calloc(n, 1);
    long deleted = 0;
    for (long c = 0; c < m; c++) {
        bool breaks = false;
        for (long i = 0; i < n - 1; i++) {
            if (!settled[i] && strs[i][c] > strs[i + 1][c]) {
                breaks = true;
                break;
            }
        }
        if (breaks) {
            deleted++;
            continue;
        }
        for (long i = 0; i < n - 1; i++) {
            if (strs[i][c] < strs[i + 1][c]) {
                settled[i] = true;
            }
        }
    }
    free(settled);
    return deleted;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

int main(void) {
    const long rounds = 120, count = 200, n = 100, m = 100;
    long seed = 955;
    char ***sets = malloc(sizeof(char **) * count);
    for (long s = 0; s < count; s++) {
        long letters = 2 + s % 3;
        char **strs = malloc(sizeof(char *) * n);
        for (long i = 0; i < n; i++) {
            strs[i] = malloc(m + 1);
            for (long c = 0; c < m; c++) {
                strs[i][c] = (char)('a' + next_random(&seed) % letters);
            }
            strs[i][m] = 0;
        }
        // a stable insertion sort by the first p letters
        long p = s % 12;
        for (long i = 1; i < n; i++) {
            for (long j = i; j > 0 && strncmp(strs[j - 1], strs[j], p) > 0; j--) {
                char *t = strs[j];
                strs[j] = strs[j - 1];
                strs[j - 1] = t;
            }
        }
        sets[s] = strs;
    }
    long total = 0, check = 0;
    for (long r = 0; r < rounds; r++) {
        for (long i = 0; i < count; i++) {
            long k = (r + i) % count;
            long d = min_deletion_size(sets[k], n, m);
            total += d;
            check = (check * 31 + d) % 1000000007;
        }
    }
    printf("%ld rounds over %ld sets of %ld strings of %ld letters: %ld columns deleted, checksum %ld\n", rounds, count, n, m, total, check);
    return 0;
}
