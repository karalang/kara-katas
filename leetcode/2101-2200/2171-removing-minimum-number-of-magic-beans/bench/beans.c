// LeetCode #2171: Removing Minimum Number of Magic Beans -- the
// benchmark's C mirror of beans.kara, over a pointer and a length.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp(const void *a, const void *b) {
    long long x = *(const long long *)a, y = *(const long long *)b;
    return (x > y) - (x < y);
}

static long long minimum_removal(const long long *beans, long long n) {
    long long *sorted = malloc(n * sizeof(long long));
    memcpy(sorted, beans, n * sizeof(long long));
    qsort(sorted, n, sizeof(long long), cmp);
    long long total = 0, kept = 0;
    for (long long i = 0; i < n; i++) {
        total += sorted[i];
        long long k = sorted[i] * (n - i);
        if (k > kept) kept = k;
    }
    free(sorted);
    return total - kept;
}

static long long seed = 2171;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    long long *row = malloc(400000 * sizeof(long long));
    for (int i = 0; i < 400000; i++) {
        long long a = next_random();
        long long b = next_random();
        row[i] = (a * 32768 + b) % 100000 + 1;
    }
    long long check = 0;
    for (int r = 0; r < 100; r++) {
        long long a = next_random();
        long long b = next_random();
        long long start = (a * 32768 + b) % 300001;
        long long removed = minimum_removal(row + start, 100000);
        check = (check * 31 + removed % 1000000007) % 1000000007;
    }
    printf("100 solves: checksum %lld\n", check);
    free(row);
    return 0;
}
