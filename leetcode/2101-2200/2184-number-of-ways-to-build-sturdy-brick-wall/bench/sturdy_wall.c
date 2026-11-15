// LeetCode #2184: Number of Ways to Build Sturdy Brick Wall -- the
// benchmark's C mirror of sturdy_wall.kara: the rows and the lists of
// rows that fit in malloc'd arrays.

#include <stdio.h>
#include <stdlib.h>

static void fill(long long at, long long joints, long long width, const long long *bricks, long long nb,
                 long long *rows, long long *n) {
    if (at == width) {
        rows[(*n)++] = joints;
        return;
    }
    for (long long i = 0; i < nb; i++) {
        long long end = at + bricks[i];
        if (end < width)
            fill(end, joints | (1LL << end), width, bricks, nb, rows, n);
        else if (end == width)
            fill(end, joints, width, bricks, nb, rows, n);
    }
}

static long long build_wall(long long height, long long width, const long long *bricks, long long nb) {
    long long *rows = malloc(1024 * sizeof(long long));
    long long n = 0;
    fill(0, 0, width, bricks, nb, rows, &n);
    long long *start = malloc((n + 1) * sizeof(long long));
    long long *fits = malloc((n * n + 1) * sizeof(long long));
    long long m = 0;
    for (long long a = 0; a < n; a++) {
        start[a] = m;
        for (long long b = 0; b < n; b++)
            if ((rows[a] & rows[b]) == 0) fits[m++] = b;
    }
    start[n] = m;
    long long *ways = malloc((n + 1) * sizeof(long long));
    long long *next = malloc((n + 1) * sizeof(long long));
    for (long long a = 0; a < n; a++) ways[a] = 1;
    for (long long h = 1; h < height; h++) {
        for (long long b = 0; b < n; b++) next[b] = 0;
        for (long long a = 0; a < n; a++)
            for (long long e = start[a]; e < start[a + 1]; e++) {
                long long b = fits[e];
                next[b] = (next[b] + ways[a]) % 1000000007;
            }
        long long *t = ways;
        ways = next;
        next = t;
    }
    long long total = 0;
    for (long long a = 0; a < n; a++) total = (total + ways[a]) % 1000000007;
    free(rows);
    free(start);
    free(fits);
    free(ways);
    free(next);
    return total;
}

static long long seed = 2184;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    long long check = 0;
    for (int r = 0; r < 1000; r++) {
        long long height = next_random() % 51 + 50;
        long long bricks[10];
        long long nb = 0;
        bricks[nb++] = 1;
        for (long long b = 2; b <= 10; b++)
            if (next_random() % 2 == 0) bricks[nb++] = b;
        check = (check * 31 + build_wall(height, 10, bricks, nb)) % 1000000007;
    }
    printf("1000 walls: checksum %lld\n", check);
    return 0;
}
