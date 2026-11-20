// LeetCode #1266 bench, in C: the ★ arm (the larger of the two gaps between
// neighbouring points, summed over each pair of neighbours) on 1000 random
// walks of 100 points from -1000 to 1000 built once, 3000 rounds; every
// answer folded into a checksum. Each point is its own two-element array,
// as LeetCode's `int[][]` is.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t gap(int64_t a, int64_t b) { return a > b ? a - b : b - a; }

static int64_t min_time_to_visit_all_points(int64_t **points, int n) {
    int64_t time = 0;
    for (int i = 1; i < n; i++) {
        int64_t dx = gap(points[i][0], points[i - 1][0]);
        int64_t dy = gap(points[i][1], points[i - 1][1]);
        time += dx > dy ? dx : dy;
    }
    return time;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1266;
    int64_t **walks[1000];
    for (int w = 0; w < 1000; w++) {
        walks[w] = malloc(100 * sizeof(int64_t *));
        for (int i = 0; i < 100; i++) {
            walks[w][i] = malloc(2 * sizeof(int64_t));
            walks[w][i][0] = next_random(&seed) % 2001 - 1000;
            walks[w][i][1] = next_random(&seed) % 2001 - 1000;
        }
    }
    int64_t check = 0;
    for (int64_t round = 0; round < 3000; round++)
        for (int w = 0; w < 1000; w++)
            check = (check * 131 + min_time_to_visit_all_points(walks[w], 100) + round) % 1000000007;
    printf("3000 rounds of 1000 walks of 100 points: checksum %lld\n", (long long)check);
    return 0;
}
