// LeetCode #1051: Height Checker -- C mirror of bench/height_checker.kara.
// The sorted copy is allocated afresh for each line, as the other
// languages' vectors are, and sorted with qsort.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long long seed = 1051;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int ascending(const void *a, const void *b) {
    long long x = *(const long long *)a, y = *(const long long *)b;
    return (x > y) - (x < y);
}

static long long height_checker(const long long *heights, int n) {
    long long *expected = malloc(n * sizeof(long long));
    memcpy(expected, heights, n * sizeof(long long));
    qsort(expected, n, sizeof(long long), ascending);
    long long moved = 0;
    for (int i = 0; i < n; i++)
        if (heights[i] != expected[i]) moved++;
    free(expected);
    return moved;
}

int main(void) {
    enum { LINES = 2000, COUNT = 100, ROUNDS = 50 };
    static long long all[LINES][COUNT];
    for (int l = 0; l < LINES; l++)
        for (int i = 0; i < COUNT; i++) all[l][i] = next_random() % 100 + 1;
    long long total = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++)
        for (int l = 0; l < LINES; l++) {
            long long answer = height_checker(all[l], COUNT);
            total += answer;
            check = (check * 131 + answer) % 1000000007;
        }
    printf("%d lines of %d students, %d rounds: total %lld, checksum %lld\n", LINES, COUNT, ROUNDS, total, check);
    return 0;
}
