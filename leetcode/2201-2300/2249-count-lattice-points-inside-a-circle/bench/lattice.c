// LeetCode #2249: Count Lattice Points Inside a Circle -- the benchmark's
// C mirror of lattice.kara: every point of the box bounding the circles
// tried against them until one holds it.
#include <stdint.h>
#include <stdio.h>

static int64_t circles[200][3];

static int64_t count_lattice_points(int n) {
    int64_t left = circles[0][0] - circles[0][2], right = circles[0][0] + circles[0][2];
    int64_t bottom = circles[0][1] - circles[0][2], top = circles[0][1] + circles[0][2];
    for (int i = 1; i < n; i++) {
        if (circles[i][0] - circles[i][2] < left) left = circles[i][0] - circles[i][2];
        if (circles[i][0] + circles[i][2] > right) right = circles[i][0] + circles[i][2];
        if (circles[i][1] - circles[i][2] < bottom) bottom = circles[i][1] - circles[i][2];
        if (circles[i][1] + circles[i][2] > top) top = circles[i][1] + circles[i][2];
    }
    int64_t count = 0;
    for (int64_t px = left; px <= right; px++)
        for (int64_t py = bottom; py <= top; py++)
            for (int i = 0; i < n; i++) {
                int64_t dx = px - circles[i][0], dy = py - circles[i][1];
                if (dx * dx + dy * dy <= circles[i][2] * circles[i][2]) {
                    count++;
                    break;
                }
            }
    return count;
}

static int64_t seed = 2249;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0;
    for (int t = 0; t < 100; t++) {
        for (int i = 0; i < 200; i++) {
            int64_t x = next_random() % 100 + 1;
            int64_t y = next_random() % 100 + 1;
            int64_t r = next_random() % (x < y ? x : y) + 1;
            circles[i][0] = x;
            circles[i][1] = y;
            circles[i][2] = r;
        }
        check = (check * 31 + count_lattice_points(200)) % 1000000007;
    }
    printf("100 cases of 200 circles: checksum %lld\n", (long long)check);
    return 0;
}
