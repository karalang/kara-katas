// LeetCode #2503: Maximum Number of Points From Grid Queries -- C mirror
// of the benchmark (points.kara): the same grids, queries, passes and
// checksum; the border in a hand-written binary min-heap of (value,
// cell), the queries' order by qsort.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SIDE 316
#define CELLS (SIDE * SIDE)
#define QUERIES 10000

static int64_t seed = 2503;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t below(int64_t top) {
    int64_t hi = next_random();
    return (hi * 32768 + next_random()) % top;
}

typedef struct {
    int64_t value, cell;
} Entry;

static int less(Entry a, Entry b) { return a.value < b.value || (a.value == b.value && a.cell < b.cell); }

static void push(Entry *heap, int64_t *len, Entry e) {
    int64_t i = (*len)++;
    while (i > 0) {
        int64_t up = (i - 1) / 2;
        if (!less(e, heap[up])) break;
        heap[i] = heap[up];
        i = up;
    }
    heap[i] = e;
}

static Entry pop(Entry *heap, int64_t *len) {
    Entry top = heap[0];
    Entry last = heap[--(*len)];
    int64_t i = 0;
    for (;;) {
        int64_t child = 2 * i + 1;
        if (child >= *len) break;
        if (child + 1 < *len && less(heap[child + 1], heap[child])) child++;
        if (!less(heap[child], last)) break;
        heap[i] = heap[child];
        i = child;
    }
    heap[i] = last;
    return top;
}

static const int64_t *sort_keys;

static int by_key(const void *a, const void *b) {
    int64_t x = sort_keys[*(const int64_t *)a], y = sort_keys[*(const int64_t *)b];
    return (x > y) - (x < y);
}

static void max_points(const int64_t *grid, const int64_t *queries, int64_t k, int64_t *answer, Entry *heap, char *seen, int64_t *order) {
    for (int64_t i = 0; i < k; i++) order[i] = i;
    sort_keys = queries;
    qsort(order, k, sizeof(int64_t), by_key);
    memset(seen, 0, CELLS);
    int64_t len = 0;
    push(heap, &len, (Entry){grid[0], 0});
    seen[0] = 1;
    int64_t reached = 0;
    static const int64_t dr[4] = {1, -1, 0, 0}, dc[4] = {0, 0, 1, -1};
    for (int64_t t = 0; t < k; t++) {
        int64_t i = order[t], q = queries[i];
        while (len > 0 && heap[0].value < q) {
            Entry e = pop(heap, &len);
            reached++;
            int64_t r = e.cell / SIDE, c = e.cell % SIDE;
            for (int d = 0; d < 4; d++) {
                int64_t rr = r + dr[d], cc = c + dc[d];
                if (rr >= 0 && rr < SIDE && cc >= 0 && cc < SIDE && !seen[rr * SIDE + cc]) {
                    seen[rr * SIDE + cc] = 1;
                    push(heap, &len, (Entry){grid[rr * SIDE + cc], rr * SIDE + cc});
                }
            }
        }
        answer[i] = reached;
    }
}

int main(void) {
    const int64_t passes = 14;
    int64_t *grids[4];
    for (int g = 0; g < 4; g++) {
        grids[g] = malloc(CELLS * sizeof(int64_t));
        for (int64_t i = 0; i < CELLS; i++) grids[g][i] = below(1000000) + 1;
    }
    int64_t *queries = malloc(QUERIES * sizeof(int64_t));
    for (int64_t i = 0; i < QUERIES; i++) queries[i] = below(1000000) + 1;
    int64_t *answer = malloc(QUERIES * sizeof(int64_t));
    int64_t *order = malloc(QUERIES * sizeof(int64_t));
    Entry *heap = malloc(CELLS * sizeof(Entry));
    char *seen = malloc(CELLS);
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++) {
        for (int g = 0; g < 4; g++) {
            int64_t r = check % SIDE, c = check / SIDE % SIDE;
            int64_t was = grids[g][r * SIDE + c];
            grids[g][r * SIDE + c] = (check + p) % 1000000 + 1;
            max_points(grids[g], queries, QUERIES, answer, heap, seen, order);
            for (int64_t i = 0; i < QUERIES; i++) check = (check * 31 + answer[i] + p) % 1000000007;
            grids[g][r * SIDE + c] = was;
        }
    }
    printf("%lld passes over 4 grids of 316 by 316, 10^4 queries: checksum %lld\n", (long long)passes, (long long)check);
    for (int g = 0; g < 4; g++) free(grids[g]);
    free(queries);
    free(answer);
    free(order);
    free(heap);
    free(seen);
    return 0;
}
