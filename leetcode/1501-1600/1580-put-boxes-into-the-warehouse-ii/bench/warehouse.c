// LeetCode #1580 bench: the same usable heights matched smallest first, in
// C, with the copies the Kara arm makes malloc'd per call and qsort for the
// sorts.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp_i64(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t max_boxes_in_warehouse(const int64_t *boxes, int64_t n, const int64_t *warehouse, int64_t m) {
    int64_t *from_left = malloc(m * sizeof(int64_t));
    int64_t *usable = malloc(m * sizeof(int64_t));
    int64_t *sorted = malloc(n * sizeof(int64_t));
    memcpy(from_left, warehouse, m * sizeof(int64_t));
    memcpy(usable, warehouse, m * sizeof(int64_t));
    memcpy(sorted, boxes, n * sizeof(int64_t));
    for (int64_t i = 1; i < m; i++)
        if (from_left[i - 1] < from_left[i]) from_left[i] = from_left[i - 1];
    for (int64_t i = m - 2; i >= 0; i--)
        if (usable[i + 1] < usable[i]) usable[i] = usable[i + 1];
    for (int64_t i = 0; i < m; i++)
        if (from_left[i] > usable[i]) usable[i] = from_left[i];
    qsort(usable, m, sizeof(int64_t), cmp_i64);
    qsort(sorted, n, sizeof(int64_t), cmp_i64);
    int64_t placed = 0;
    for (int64_t i = 0; i < m; i++)
        if (placed < n && sorted[placed] <= usable[i]) placed++;
    free(from_left);
    free(usable);
    free(sorted);
    return placed;
}

static int64_t seed = 1580;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    enum { P = 40, N = 100000 };
    int64_t *boxes[P], *warehouse[P];
    for (int p = 0; p < P; p++) {
        boxes[p] = malloc(N * sizeof(int64_t));
        warehouse[p] = malloc(N * sizeof(int64_t));
        for (int64_t i = 0; i < N; i++) boxes[p][i] = (next_random() * 32768 + next_random()) % 1000000000 + 1;
        for (int64_t i = 0; i < N; i++) {
            int64_t d = i - 50000;
            int64_t valley = (d < 0 ? -d : d) * 20000;
            warehouse[p][i] = valley + (next_random() * 32768 + next_random()) % 1000000;
        }
    }
    int64_t check = 0, total = 0;
    for (int p = 0; p < P; p++) {
        int64_t placed = max_boxes_in_warehouse(boxes[p], N, warehouse[p], N);
        total += placed;
        check = mix(check, placed);
    }
    printf("40 problems of 100000 boxes and rooms: boxes placed %lld, checksum %lld\n", (long long)total,
           (long long)check);
    for (int p = 0; p < P; p++) {
        free(boxes[p]);
        free(warehouse[p]);
    }
    return 0;
}
