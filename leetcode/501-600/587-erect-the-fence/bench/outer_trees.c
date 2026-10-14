// Benchmark for #587: C mirror of the ★ arm (the monotone chain); see
// outer_trees.kara. Each call copies the trees into a fresh array, sorts
// it with `qsort`, builds the fence in a second array, sorts that and
// removes repeats.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t x, y;
} Point;

static int compare(const void *pa, const void *pb) {
    const Point *a = pa, *b = pb;
    if (a->x != b->x) return a->x < b->x ? -1 : 1;
    if (a->y != b->y) return a->y < b->y ? -1 : 1;
    return 0;
}

static int64_t cross(Point o, Point a, Point b) {
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x);
}

static Point *outer_trees(const Point *trees, int64_t n, int64_t *out_len) {
    Point *points = malloc(sizeof(Point) * n);
    memcpy(points, trees, sizeof(Point) * n);
    qsort(points, n, sizeof(Point), compare);
    Point *fence = malloc(sizeof(Point) * 2 * n);
    int64_t len = 0;
    for (int64_t i = 0; i < n; i++) {
        while (len >= 2 && cross(fence[len - 2], fence[len - 1], points[i]) < 0) len--;
        fence[len++] = points[i];
    }
    int64_t lower = len;
    for (int64_t i = n - 1; i >= 0; i--) {
        while (len > lower && cross(fence[len - 2], fence[len - 1], points[i]) < 0) len--;
        fence[len++] = points[i];
    }
    qsort(fence, len, sizeof(Point), compare);
    int64_t kept = 0;
    for (int64_t i = 0; i < len; i++) {
        if (kept == 0 || compare(&fence[i], &fence[kept - 1]) != 0) fence[kept++] = fence[i];
    }
    free(points);
    *out_len = kept;
    return fence;
}

// ---- benchmark --------------------------------------------------------------

static int64_t seed = 587;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t count = 50, rounds = 300;
    Point *gardens[50];
    int64_t sizes[50];
    for (int64_t g = 0; g < count; g++) {
        int64_t size = 1000 + next_random() % 2001;
        char taken[101 * 101] = {0};
        gardens[g] = malloc(sizeof(Point) * size);
        int64_t len = 0;
        while (len < size) {
            int64_t x = next_random() % 101;
            int64_t y = next_random() % 101;
            if (!taken[x * 101 + y]) {
                taken[x * 101 + y] = 1;
                gardens[g][len].x = x;
                gardens[g][len].y = y;
                len++;
            }
        }
        sizes[g] = size;
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int64_t g = 0; g < count; g++) {
            int64_t p = (round * 7 + g) % count;
            int64_t len;
            Point *fence = outer_trees(gardens[p], sizes[p], &len);
            int64_t sum = 0;
            for (int64_t i = 0; i < len; i++) sum += fence[i].x * 101 + fence[i].y;
            total += len;
            checksum = (checksum * 31 + sum) % 1000000007;
            free(fence);
        }
    }
    printf("%lld gardens, %lld rounds: %lld on the fence, checksum %lld\n",
           (long long)count, (long long)rounds, (long long)total, (long long)checksum);
    for (int64_t g = 0; g < count; g++) free(gardens[g]);
    return 0;
}
