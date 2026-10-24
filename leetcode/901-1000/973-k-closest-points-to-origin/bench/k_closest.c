// Benchmark: LeetCode #973 K Closest Points to Origin -- the ★ arm, sort
// by squared distance, on 100 sets of 1000 random points. Mirrors
// k_closest.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int64_t x, y; } Point;

static int by_distance(const void *a, const void *b) {
    const Point *p = a, *q = b;
    int64_t dp = p->x * p->x + p->y * p->y, dq = q->x * q->x + q->y * q->y;
    return (dp > dq) - (dp < dq);
}

static int by_value(const void *a, const void *b) {
    int64_t p = *(const int64_t *)a, q = *(const int64_t *)b;
    return (p > q) - (p < q);
}

// Writes the k closest of points[0..n) into out; returns k.
static int64_t k_closest(const Point *points, int64_t n, int64_t k, Point *out) {
    memcpy(out, points, (size_t)n * sizeof(Point));
    qsort(out, (size_t)n, sizeof(Point), by_distance);
    return k;
}

static int64_t seed = 973;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

#define N 1000
#define COUNT 100

static Point cases[COUNT][N];
static int64_t ks[COUNT];

static void random_case(Point *points, int64_t n, int64_t *k_out) {
    int64_t ds[N];
    for (int64_t i = 0; i < n; i++) {
        points[i].x = next_random() % 20001 - 10000;
        points[i].y = next_random() % 20001 - 10000;
        ds[i] = points[i].x * points[i].x + points[i].y * points[i].y;
    }
    qsort(ds, (size_t)n, sizeof(int64_t), by_value);
    int64_t k = 1 + next_random() % n;
    while (k < n && ds[k - 1] == ds[k]) k++;
    *k_out = k;
}

int main(void) {
    int64_t rounds = 100;
    for (int c = 0; c < COUNT; c++) random_case(cases[c], N, &ks[c]);
    Point out[N];
    int64_t kept = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < COUNT; i++) {
            int64_t c = (r + i) % COUNT;
            int64_t len = k_closest(cases[c], N, ks[c], out);
            kept += len;
            for (int64_t j = 0; j < len; j++) {
                int64_t v = ((out[j].x + 10001) * 20003 + out[j].y + 10001) % 1000000007;
                check = (check + v * v) % 1000000007;
            }
        }
    }
    printf("%lld rounds over %d sets of 1000 points: %lld points kept, checksum %lld\n",
           (long long)rounds, COUNT, (long long)kept, (long long)check);
    return 0;
}
