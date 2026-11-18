// LeetCode #2280: Minimum Lines to Represent a Line Chart -- the bench,
// the ★ arm. Each point is a pair of `int64_t`, day then price.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t day, price;
} Point;

static int by_day(const void *a, const void *b) {
    int64_t x = ((const Point *)a)->day, y = ((const Point *)b)->day;
    return (x > y) - (x < y);
}

static int64_t minimum_lines(const Point *stock_prices, int64_t n) {
    Point *points = malloc(n * sizeof(Point));
    for (int64_t i = 0; i < n; i++) points[i] = stock_prices[i];
    qsort(points, n, sizeof(Point), by_day);
    int64_t lines = 0;
    if (n >= 2) {
        lines = 1;
        for (int64_t i = 2; i < n; i++) {
            Point a = points[i - 2], b = points[i - 1], c = points[i];
            if ((b.price - a.price) * (c.day - b.day) != (c.price - b.price) * (b.day - a.day)) lines++;
        }
    }
    free(points);
    return lines;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2280;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0;
    Point *points = malloc(100000 * sizeof(Point));
    for (int t = 0; t < 20; t++) {
        int64_t len = 0, day = 1, price = 500000000;
        while (len < 100000) {
            int64_t dx = next_random() % 1000 + 1;
            int64_t dy = next_random() % 2001 - 1000;
            int64_t run = next_random() % 5 + 1;
            for (int64_t r = 0; r < run; r++) {
                if (len < 100000) {
                    points[len].day = day;
                    points[len].price = price;
                    len++;
                    day += dx;
                    price += dy;
                }
            }
        }
        for (int64_t i = 99999; i >= 1; i--) {
            int64_t high = next_random();
            int64_t j = (high * 32768 + next_random()) % (i + 1);
            Point s = points[i];
            points[i] = points[j];
            points[j] = s;
        }
        check = (check * 31 + minimum_lines(points, 100000)) % 1000000007;
    }
    free(points);
    printf("20 charts of 10^5: checksum %lld\n", (long long)check);
    return 0;
}
