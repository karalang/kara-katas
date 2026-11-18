// LeetCode #1610: Maximum Number of Visible Points -- the bench in C,
// mirroring visible.kara: each direction in degrees (`atan2` times
// 180 / pi, as Rust's `to_degrees`), sorted with qsort and doubled with
// 360 more, and a window slid along it.
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define PROBLEMS 20
#define N 100000

static int by_value(const void *a, const void *b) {
    double x = *(const double *)a, y = *(const double *)b;
    return (x > y) - (x < y);
}

static int visible_points(const int32_t *xs, const int32_t *ys, int n, int angle, int lx, int ly, double *dirs) {
    int here = 0, m = 0;
    for (int i = 0; i < n; i++) {
        int dx = xs[i] - lx, dy = ys[i] - ly;
        if (dx == 0 && dy == 0) here++;
        else dirs[m++] = atan2((double)dy, (double)dx) * (180.0 / M_PI);
    }
    qsort(dirs, m, sizeof(double), by_value);
    for (int i = 0; i < m; i++) dirs[m + i] = dirs[i] + 360.0;
    double reach = (double)angle + 1e-9;
    int best = 0, j = 0;
    for (int i = 0; i < 2 * m; i++) {
        while (dirs[i] - dirs[j] > reach) j++;
        if (i - j + 1 > best) best = i - j + 1;
    }
    return best + here;
}

static int64_t seed = 1610;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int32_t *xs = malloc(sizeof(int32_t) * PROBLEMS * N), *ys = malloc(sizeof(int32_t) * PROBLEMS * N);
    int angle[PROBLEMS], lx[PROBLEMS], ly[PROBLEMS];
    for (int p = 0; p < PROBLEMS; p++) {
        for (int i = 0; i < N; i++) {
            xs[p * N + i] = (int32_t)(next_random() % 101);
            ys[p * N + i] = (int32_t)(next_random() % 101);
        }
        angle[p] = (int)(next_random() % 360);
        lx[p] = (int)(next_random() % 101);
        ly[p] = (int)(next_random() % 101);
    }
    double *dirs = malloc(sizeof(double) * 2 * N);
    int64_t check = 0, visible = 0;
    for (int p = 0; p < PROBLEMS; p++) {
        int v = visible_points(xs + p * N, ys + p * N, N, angle[p], lx[p], ly[p], dirs);
        check = (check * 31 + v + 1) % 1000000007;
        visible += v;
    }
    printf("20 problems of 100000 points from 0 to 100: %lld visible, checksum %lld\n", (long long)visible,
           (long long)check);
    free(dirs); free(xs); free(ys);
    return 0;
}
