// Benchmark for #469: mirror of convex_polygon.kara (the ★ arm: the sign
// of every turn) on the same workload.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t x, y;
} Point;

static bool is_convex(const Point *points, int64_t n) {
    int sign = 0;
    for (int64_t i = 0; i < n; i++) {
        Point p0 = points[i];
        Point p1 = points[(i + 1) % n];
        Point p2 = points[(i + 2) % n];
        int64_t cross = (p1.x - p0.x) * (p2.y - p1.y) - (p1.y - p0.y) * (p2.x - p1.x);
        if (cross != 0) {
            int s = cross > 0 ? 1 : -1;
            if (sign == 0) {
                sign = s;
            } else if (s != sign) {
                return false;
            }
        }
    }
    return true;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static Point *polygon(int64_t n, bool dent, int64_t *seed) {
    Point *points = malloc(sizeof(Point) * (size_t)n);
    int64_t x = -(n * 2);
    for (int64_t i = 0; i < n; i++) {
        points[i] = (Point){x, x * x};
        x += 1 + next_random(seed) % 3;
    }
    if (dent) {
        int64_t i = 1 + next_random(seed) % (n - 2);
        int64_t xa = points[i - 1].x, xb = points[i].x, yb = points[i].y, xc = points[i + 1].x;
        points[i] = (Point){xb, yb + (xb - xa) * (xc - xb) + 1};
    }
    return points;
}

int main(void) {
    const int64_t count = 100;
    const int64_t n = 50000;
    const int64_t rounds = 20;
    int64_t seed = 469;
    Point **polygons = malloc(sizeof(Point *) * (size_t)count);
    for (int64_t k = 0; k < count; k++) {
        polygons[k] = polygon(n, k % 2 == 1, &seed);
    }
    int64_t convex = 0, checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t k = 0; k < count; k++) {
            bool answer = is_convex(polygons[k], n);
            if (answer) {
                convex += 1;
            }
            checksum = (checksum * 3 + (answer ? 1 : 2) + r) % 1000000007;
        }
    }
    printf("%lld rounds on %lld polygons of %lld vertices: %lld convex, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)n, (long long)convex, (long long)checksum);
    for (int64_t k = 0; k < count; k++) {
        free(polygons[k]);
    }
    free(polygons);
    return 0;
}
