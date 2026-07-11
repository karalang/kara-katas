/*
 * Benchmark workload — Largest Rectangle in Histogram (LeetCode #84).
 * C mirror of bench/largest_rectangle.kara (SEQ lane). Each iteration builds a fresh
 * sawtooth histogram (heights[j] = (j + iter) % 50, N=2000) as a malloc'd array, runs
 * the monotonic-stack largest_rectangle (its stack a fresh malloc'd array), and adds
 * the area into an associative sum. Same N/K. The largest_rectangle_par.c sibling
 * parallelises the same reduction with pthreads. See ../README.md § Benchmarks.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int64_t largest_rectangle(const int64_t *heights, int64_t n) {
    int64_t *stack = (int64_t *)malloc((n + 1) * sizeof(int64_t));
    int64_t sp = 0;                 /* stack size */
    int64_t max_area = 0;
    for (int64_t i = 0; i <= n; i++) {
        int64_t h = (i < n) ? heights[i] : 0;
        while (sp > 0 && heights[stack[sp - 1]] > h) {
            int64_t top = stack[--sp];
            int64_t height = heights[top];
            int64_t width = (sp == 0) ? i : (i - stack[sp - 1] - 1);
            int64_t area = height * width;
            if (area > max_area) max_area = area;
        }
        stack[sp++] = i;
    }
    free(stack);
    return max_area;
}

static int64_t *build(int64_t n, int64_t iter) {
    int64_t *h = (int64_t *)malloc(n * sizeof(int64_t));
    for (int64_t j = 0; j < n; j++)
        h[j] = (j + iter) % 50;
    return h;
}

int main(void) {
    const int64_t n = 2000, total = 108000;
    int64_t sum = 0;
    for (int64_t k = 0; k < total; k++) {
        int64_t *h = build(n, k);
        sum += largest_rectangle(h, n);
        free(h);
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
