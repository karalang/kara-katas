// LeetCode #1828: Queries on Number of Points Inside a Circle -- the bench in
// C: the ★ arm over 200 calls on runs of 250 to 499 points and 250 to 499
// queries cut from one list of 1000 points and one of 1000 queries of radius 1
// to 500, built once, each run's start and lengths drawn from the checksum so
// far. Each call copies its runs, as the arm takes its lists by value.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// points as n rows of 2, queries as m rows of 3; the counts go to answer
static void count_points(const int64_t *points, int64_t n, const int64_t *queries, int64_t m, int64_t *answer) {
    for (int64_t j = 0; j < m; j++) {
        int64_t x = queries[3 * j], y = queries[3 * j + 1], r = queries[3 * j + 2];
        int64_t inside = 0;
        for (int64_t i = 0; i < n; i++) {
            int64_t dx = points[2 * i] - x, dy = points[2 * i + 1] - y;
            if (dx * dx + dy * dy <= r * r) inside++;
        }
        answer[j] = inside;
    }
}

static int64_t seed = 1828;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t *points = malloc(2000 * sizeof(int64_t)), *queries = malloc(3000 * sizeof(int64_t));
    for (int i = 0; i < 1000; i++) {
        points[2 * i] = next_random() % 501;
        points[2 * i + 1] = next_random() % 501;
    }
    for (int i = 0; i < 1000; i++) {
        queries[3 * i] = next_random() % 501;
        queries[3 * i + 1] = next_random() % 501;
        queries[3 * i + 2] = 1 + next_random() % 500;
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 200; call++) {
        int64_t from = (check + call) % 500;
        int64_t n = 250 + (check * 7 + call) % 250;
        int64_t m = 250 + (check * 13 + call) % 250;
        int64_t *p = malloc((size_t)(2 * n) * sizeof(int64_t)), *q = malloc((size_t)(3 * m) * sizeof(int64_t));
        memcpy(p, points + 2 * from, (size_t)(2 * n) * sizeof(int64_t));
        memcpy(q, queries + 3 * from, (size_t)(3 * m) * sizeof(int64_t));
        int64_t *answer = malloc((size_t)m * sizeof(int64_t));
        count_points(p, n, q, m, answer);
        for (int64_t j = 0; j < m; j++) check = (check * 31 + answer[j]) % 1000000007;
        free(p);
        free(q);
        free(answer);
    }
    printf("200 calls: checksum %lld\n", (long long)check);
    free(points);
    free(queries);
    return 0;
}
