// LeetCode #1564: Put Boxes Into the Warehouse I -- bench: the ★ arm
// (usable heights, the smallest boxes into the deepest rooms) over 20
// problems of 100000 boxes and 100000 rooms, built once, each asked 10
// times.
// C mirror of warehouse.kara; the boxes' copy is sorted by qsort.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100000

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t max_boxes_in_warehouse(const int64_t *boxes, int64_t n, const int64_t *warehouse, int64_t m) {
    int64_t *usable = malloc(m * sizeof(int64_t));
    memcpy(usable, warehouse, m * sizeof(int64_t));
    for (int64_t i = 1; i < m; i++)
        if (usable[i - 1] < usable[i]) usable[i] = usable[i - 1];
    int64_t *sorted = malloc(n * sizeof(int64_t));
    memcpy(sorted, boxes, n * sizeof(int64_t));
    qsort(sorted, n, sizeof(int64_t), cmp);
    int64_t placed = 0;
    for (int64_t r = m - 1; r >= 0; r--)
        if (placed < n && sorted[placed] <= usable[r]) placed++;
    free(usable);
    free(sorted);
    return placed;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    const int64_t top = 1000000000;
    int64_t seed = 1564;
    static int64_t boxes[20][N], warehouse[20][N];
    for (int p = 0; p < 20; p++) {
        for (int i = 0; i < N; i++) {
            int64_t v = next_random(&seed) * 32768;
            boxes[p][i] = (v + next_random(&seed)) % top + 1;
        }
        for (int i = 0; i < N; i++) {
            int64_t v = next_random(&seed) * 32768;
            warehouse[p][i] = top - (v + next_random(&seed)) % ((top + 1) / 2);
        }
    }
    int64_t check = 0, total = 0;
    for (int pass = 0; pass < 10; pass++)
        for (int p = 0; p < 20; p++) {
            int64_t placed = max_boxes_in_warehouse(boxes[p], N, warehouse[p], N);
            total += placed;
            check = mix(check, placed);
        }
    printf("10 passes over 20 problems of 100000 boxes and rooms: %lld boxes, checksum %lld\n", (long long)total,
           (long long)check);
    return 0;
}
