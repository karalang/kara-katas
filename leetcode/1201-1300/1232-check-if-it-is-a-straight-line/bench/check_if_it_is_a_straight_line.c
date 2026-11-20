// LeetCode #1232 bench: the ★ arm in C, over the same 1000 sets of 1000
// points and 200 passes as the Kāra bench.
#include <stdio.h>
#include <stdlib.h>

static int check_straight_line(const long *pts, long n) {
    long dx = pts[2] - pts[0], dy = pts[3] - pts[1];
    for (long i = 0; i < n; i++)
        if ((pts[2 * i] - pts[0]) * dy != (pts[2 * i + 1] - pts[1]) * dx) return 0;
    return 1;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

int main(void) {
    long seed = 1232;
    long *sets = malloc(sizeof(long) * 1000 * 2000);
    for (int s = 0; s < 1000; s++) {
        long dx = next_random(&seed) % 21 - 10;
        long dy = next_random(&seed) % 21 - 10;
        if (dx == 0 && dy == 0) dx = 1;
        long *pts = sets + (long)s * 2000;
        for (long t = 0; t < 1000; t++) {
            pts[2 * t] = t * dx;
            pts[2 * t + 1] = t * dy;
        }
        if (s % 2 == 1) {
            if (dx == 0) pts[1998] += 1;
            else pts[1999] += 1;
        }
    }
    long straight = 0;
    for (int pass = 0; pass < 200; pass++)
        for (int s = 0; s < 1000; s++)
            straight += check_straight_line(sets + (long)s * 2000, 1000);
    printf("1000 sets of 1000 points, 200 passes: %ld straight\n", straight);
    free(sets);
    return 0;
}
