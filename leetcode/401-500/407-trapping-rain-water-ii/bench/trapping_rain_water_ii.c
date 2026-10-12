// Benchmark for #407: mirror of trapping_rain_water_ii.kara (a min-heap
// walking in from the border). C has no heap type, so its mirror carries a
// binary min-heap of (level, row, column) ordered as the tuples are in
// the other mirrors.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t level, r, c;
} Cell;

static int less(Cell a, Cell b) {
    if (a.level != b.level) return a.level < b.level;
    if (a.r != b.r) return a.r < b.r;
    return a.c < b.c;
}

typedef struct {
    Cell *items;
    int64_t len, cap;
} Heap;

static void heap_push(Heap *h, Cell x) {
    if (h->len == h->cap) {
        h->cap = h->cap ? h->cap * 2 : 64;
        h->items = realloc(h->items, h->cap * sizeof(Cell));
    }
    int64_t i = h->len++;
    while (i > 0) {
        int64_t p = (i - 1) / 2;
        if (!less(x, h->items[p])) break;
        h->items[i] = h->items[p];
        i = p;
    }
    h->items[i] = x;
}

static Cell heap_pop(Heap *h) {
    Cell top = h->items[0];
    Cell x = h->items[--h->len];
    int64_t i = 0;
    for (;;) {
        int64_t l = 2 * i + 1, r = l + 1, s = i;
        Cell best = x;
        if (l < h->len && less(h->items[l], best)) { s = l; best = h->items[l]; }
        if (r < h->len && less(h->items[r], best)) { s = r; }
        if (s == i) break;
        h->items[i] = h->items[s];
        i = s;
    }
    h->items[i] = x;
    return top;
}

static int64_t trap_rain_water(int64_t *height, int64_t m, int64_t n) {
    if (m < 3 || n < 3) return 0;
    char *seen = calloc(m * n, 1);
    Heap h = {0};
    for (int64_t r = 0; r < m; r++) {
        for (int64_t c = 0; c < n; c++) {
            if (r == 0 || c == 0 || r == m - 1 || c == n - 1) {
                heap_push(&h, (Cell){height[r * n + c], r, c});
                seen[r * n + c] = 1;
            }
        }
    }
    static const int64_t dr[4] = {1, -1, 0, 0};
    static const int64_t dc[4] = {0, 0, 1, -1};
    int64_t water = 0;
    while (h.len > 0) {
        Cell t = heap_pop(&h);
        for (int d = 0; d < 4; d++) {
            int64_t nr = t.r + dr[d], nc = t.c + dc[d];
            if (nr >= 0 && nr < m && nc >= 0 && nc < n && !seen[nr * n + nc]) {
                seen[nr * n + nc] = 1;
                int64_t ht = height[nr * n + nc];
                if (ht < t.level) water += t.level - ht;
                heap_push(&h, (Cell){ht > t.level ? ht : t.level, nr, nc});
            }
        }
    }
    free(h.items);
    free(seen);
    return water;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(int argc, char **argv) {
    int64_t grids = argc > 1 ? atoll(argv[1]) : 60;
    int64_t size = 200;
    int64_t seed = 407, total = 0, checksum = 0;
    int64_t *grid = malloc(size * size * sizeof(int64_t));
    for (int64_t g = 0; g < grids; g++) {
        for (int64_t i = 0; i < size * size; i++) {
            int64_t hi = step(&seed);
            grid[i] = (hi * 32768 + step(&seed)) % 20000;
        }
        int64_t w = trap_rain_water(grid, size, size);
        total += w;
        checksum = (checksum * 31 + w) % 1000000007;
    }
    free(grid);
    printf("%lld grids of %lld x %lld: %lld units of water, checksum %lld\n", (long long)grids, (long long)size, (long long)size, (long long)total, (long long)checksum);
    return 0;
}
