// LeetCode 812 -- Largest Triangle Area: the bench, with the ★ arm's
// every triple of points.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 812;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

typedef struct {
    int64_t x, y;
} Point;

static int64_t twice_area(Point a, Point b, Point c) {
    return llabs((b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x));
}

static double largest_triangle_area(const Point *points, int64_t n) {
    int64_t best = 0;
    for (int64_t i = 0; i < n; i++) {
        for (int64_t j = i + 1; j < n; j++) {
            for (int64_t k = j + 1; k < n; k++) {
                int64_t twice = twice_area(points[i], points[j], points[k]);
                if (twice > best) {
                    best = twice;
                }
            }
        }
    }
    return (double)best / 2.0;
}

// A point with coordinates from -50 to 50 that is not in `points`.
static Point new_point(const Point *points, int64_t n) {
    for (;;) {
        Point p;
        p.x = next_random() % 101 - 50;
        p.y = next_random() % 101 - 50;
        int taken = 0;
        for (int64_t i = 0; i < n; i++) {
            if (points[i].x == p.x && points[i].y == p.y) {
                taken = 1;
            }
        }
        if (!taken) {
            return p;
        }
    }
}

// 64 sets of 50 distinct points are made once. Each round moves one point
// of the next set to a new place and finds that set's largest triangle.
int main(void) {
    static Point sets[64][50];
    for (int k = 0; k < 64; k++) {
        for (int i = 0; i < 50; i++) {
            sets[k][i] = new_point(sets[k], i);
        }
    }
    int64_t rounds = 60000;
    double total = 0.0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t k = r % 64;
        Point p = new_point(sets[k], 50);
        sets[k][r / 64 % 50] = p;
        double area = largest_triangle_area(sets[k], 50);
        total += area;
        check = (check * 131 + (int64_t)(area * 2.0)) % 1000000007;
    }
    printf("%lld rounds of 50 points: total area %.1f, checksum %lld\n",
           (long long)rounds, total, (long long)check);
    return 0;
}
