// LeetCode #1401 bench, C: the same clamp and squared distance, workload
// and checksum as check_overlap.kara; a case is a row of seven ints.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static int32_t clamp(int32_t v, int32_t lo, int32_t hi) {
    return v < lo ? lo : v > hi ? hi : v;
}

static bool check_overlap(int32_t radius, int32_t x_center, int32_t y_center, int32_t x1,
                          int32_t y1, int32_t x2, int32_t y2) {
    int32_t dx = clamp(x_center, x1, x2) - x_center;
    int32_t dy = clamp(y_center, y1, y2) - y_center;
    return dx * dx + dy * dy <= radius * radius;
}

int main(void) {
    static int32_t cases[N][7];
    int64_t seed = 1401;
    for (int i = 0; i < N; i++) {
        for (int k = 0; k < 5; k++) {
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            cases[i][k] = (int32_t)(seed % 2001 - 1000);
        }
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        int32_t w = (int32_t)(1 + seed % 300);
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        int32_t h = (int32_t)(1 + seed % 300);
        cases[i][0] = abs(cases[i][0]) / 10 + 1;
        cases[i][5] = cases[i][3] + w;
        cases[i][6] = cases[i][4] + h;
    }
    int64_t check = 0;
    for (int32_t round = 0; round < 1000; round++) {
        int64_t overlaps = 0;
        for (int i = 0; i < N; i++) {
            int32_t *c = cases[i];
            if (check_overlap(c[0] + round, c[1], c[2], c[3], c[4], c[5], c[6])) {
                overlaps++;
            }
        }
        check = (check * 131 + overlaps) % 1000000007;
    }
    printf("1000 rounds over 10^5 circles and rectangles: checksum %lld\n", (long long)check);
    return 0;
}
