// LeetCode #1066: Campus Bikes II -- the benchmark, the same table over
// the sets of bikes taken as campus_bikes.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t x, y;
} Point;

static int64_t distance(Point a, Point b) { return llabs(a.x - b.x) + llabs(a.y - b.y); }

static int64_t assign_bikes(const Point *workers, int64_t n, const Point *bikes, int64_t m) {
    int64_t size = (int64_t)1 << m;
    int64_t *best = malloc(size * sizeof *best);
    for (int64_t k = 0; k < size; k++) best[k] = INT64_MAX;
    best[0] = 0;
    int64_t answer = INT64_MAX;
    for (int64_t mask = 0; mask < size; mask++) {
        if (best[mask] == INT64_MAX) continue;
        int64_t w = __builtin_popcountll(mask);
        if (w == n) {
            if (best[mask] < answer) answer = best[mask];
            continue;
        }
        for (int64_t b = 0; b < m; b++) {
            if ((mask & ((int64_t)1 << b)) == 0) {
                int64_t next = mask | ((int64_t)1 << b);
                int64_t t = best[mask] + distance(workers[w], bikes[b]);
                if (t < best[next]) best[next] = t;
            }
        }
    }
    free(best);
    return answer;
}

static int64_t seed = 1066;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static void random_points(Point *out, int64_t n) {
    for (int64_t i = 0; i < n; i++) {
        out[i].x = next_random() % 1000;
        out[i].y = next_random() % 1000;
    }
}

int main(void) {
    // 5000 problems of 8 to 10 workers and 10 bikes on a 1000 by 1000
    // grid, built once, then each answered
    static Point workers[5000][10], bikes[5000][10];
    static int64_t counts[5000];
    for (int p = 0; p < 5000; p++) {
        counts[p] = 8 + next_random() % 3;
        random_points(workers[p], counts[p]);
        random_points(bikes[p], 10);
    }
    int64_t calls = 0, total = 0, check = 0;
    for (int p = 0; p < 5000; p++) {
        int64_t answer = assign_bikes(workers[p], counts[p], bikes[p], 10);
        total += answer;
        check = (check * 31 + answer) % 1000000007;
        calls++;
    }
    printf("%lld calls: answers sum %lld, checksum %lld\n", (long long)calls, (long long)total,
           (long long)check);
    return 0;
}
