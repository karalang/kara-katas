// LeetCode #1631: Path With Minimum Effort -- the bench's C mirror: the ★
// arm on 200 random grids of 100 x 100 heights up to 10^6, all drawn
// first, with a binary min-heap of (effort, row, column) written out.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

enum { GRIDS = 200, R = 100, C = 100 };

typedef struct {
    int32_t effort;
    int64_t r, c;
} Entry;

static int less(Entry a, Entry b) {
    if (a.effort != b.effort) return a.effort < b.effort;
    if (a.r != b.r) return a.r < b.r;
    return a.c < b.c;
}

typedef struct {
    Entry *items;
    size_t len, cap;
} Heap;

static void heap_push(Heap *h, Entry e) {
    if (h->len == h->cap) {
        h->cap = h->cap ? 2 * h->cap : 64;
        h->items = realloc(h->items, sizeof(Entry) * h->cap);
    }
    size_t i = h->len++;
    while (i > 0) {
        size_t p = (i - 1) / 2;
        if (!less(e, h->items[p])) break;
        h->items[i] = h->items[p];
        i = p;
    }
    h->items[i] = e;
}

static Entry heap_pop(Heap *h) {
    Entry top = h->items[0], last = h->items[--h->len];
    size_t i = 0;
    for (;;) {
        size_t l = 2 * i + 1, r = l + 1, m = i;
        Entry best = last;
        if (l < h->len && less(h->items[l], best)) m = l, best = h->items[l];
        if (r < h->len && less(h->items[r], best)) m = r;
        if (m == i) break;
        h->items[i] = h->items[m];
        i = m;
    }
    if (h->len) h->items[i] = last;
    return top;
}

static int32_t minimum_effort_path(int32_t heights[R][C], int64_t rows, int64_t cols) {
    static int32_t best[R][C];
    for (int64_t r = 0; r < rows; r++)
        for (int64_t c = 0; c < cols; c++) best[r][c] = INT32_MAX;
    Heap queue = {0};
    best[0][0] = 0;
    heap_push(&queue, (Entry){0, 0, 0});
    static const int64_t dirs[4][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    int32_t answer = 0;
    while (queue.len) {
        Entry e = heap_pop(&queue);
        if (e.r == rows - 1 && e.c == cols - 1) {
            answer = e.effort;
            break;
        }
        if (e.effort > best[e.r][e.c]) continue;
        for (int d = 0; d < 4; d++) {
            int64_t nr = e.r + dirs[d][0], nc = e.c + dirs[d][1];
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
            int32_t diff = abs(heights[nr][nc] - heights[e.r][e.c]);
            int32_t step = e.effort > diff ? e.effort : diff;
            if (step < best[nr][nc]) {
                best[nr][nc] = step;
                heap_push(&queue, (Entry){step, nr, nc});
            }
        }
    }
    free(queue.items);
    return answer;
}

static int64_t seed = 1631;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int32_t grids[GRIDS][R][C];
    for (int g = 0; g < GRIDS; g++)
        for (int r = 0; r < R; r++)
            for (int c = 0; c < C; c++) {
                int64_t high = next_random();
                grids[g][r][c] = (int32_t)((high * 32768 + next_random()) % 1000000 + 1);
            }
    int64_t check = 0, total = 0;
    for (int g = 0; g < GRIDS; g++) {
        int64_t effort = minimum_effort_path(grids[g], R, C);
        total += effort;
        check = (check * 31 + effort + 1) % 1000000007;
    }
    printf("200 grids of 100 x 100: efforts sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
