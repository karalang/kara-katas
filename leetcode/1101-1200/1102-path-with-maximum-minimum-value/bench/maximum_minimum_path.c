// Benchmark: LeetCode #1102 Path With Maximum Minimum Value -- a
// best-first search with a binary max-heap of (minimum, row, column),
// compared as tuples, as the Kāra ★ arm. Mirrors maximum_minimum_path.kara.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100

typedef struct { int64_t low, r, c; } Entry;

static bool above(Entry a, Entry b) {
    if (a.low != b.low) return a.low > b.low;
    if (a.r != b.r) return a.r > b.r;
    return a.c > b.c;
}

typedef struct { Entry *data; size_t len, cap; } Heap;

static void push(Heap *h, Entry e) {
    if (h->len == h->cap) {
        h->cap = h->cap ? 2 * h->cap : 16;
        h->data = realloc(h->data, h->cap * sizeof(Entry));
    }
    size_t i = h->len++;
    while (i > 0 && above(e, h->data[(i - 1) / 2])) {
        h->data[i] = h->data[(i - 1) / 2];
        i = (i - 1) / 2;
    }
    h->data[i] = e;
}

static Entry pop(Heap *h) {
    Entry top = h->data[0], last = h->data[--h->len];
    size_t i = 0;
    for (;;) {
        size_t l = 2 * i + 1, best = i;
        Entry b = last;
        if (l < h->len && above(h->data[l], b)) { best = l; b = h->data[l]; }
        if (l + 1 < h->len && above(h->data[l + 1], b)) { best = l + 1; }
        if (best == i) break;
        h->data[i] = h->data[best];
        i = best;
    }
    if (h->len > 0) h->data[i] = last;
    return top;
}

static int64_t maximum_minimum_path(int64_t grid[N][N]) {
    bool *done = calloc(N * N, sizeof(bool));
    Heap h = {0};
    push(&h, (Entry){grid[0][0], 0, 0});
    static const int dr[4] = {0, 1, 0, -1}, dc[4] = {1, 0, -1, 0};
    int64_t answer = -1;
    while (h.len > 0) {
        Entry e = pop(&h);
        if (done[e.r * N + e.c]) continue;
        done[e.r * N + e.c] = true;
        if (e.r == N - 1 && e.c == N - 1) { answer = e.low; break; }
        for (int d = 0; d < 4; d++) {
            int64_t nr = e.r + dr[d], nc = e.c + dc[d];
            if (nr >= 0 && nr < N && nc >= 0 && nc < N && !done[nr * N + nc]) {
                int64_t v = grid[nr][nc];
                push(&h, (Entry){e.low < v ? e.low : v, nr, nc});
            }
        }
    }
    free(h.data);
    free(done);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1102;
    static int64_t grids[32][N][N];
    for (int g = 0; g < 32; g++)
        for (int r = 0; r < N; r++)
            for (int c = 0; c < N; c++) grids[g][r][c] = next_random(&seed) * 30517 % 1000000000;
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 8; round++)
        for (int64_t j = 0; j < 32; j++) {
            int64_t at = (round * 7919 + j * 104729) % 10000;
            grids[j][at / 100][at % 100] /= 2;
            int64_t best = maximum_minimum_path(grids[j]);
            total += best;
            check = (check * 31 + best % 1000003 + 1) % 1000000007;
        }
    printf("8 rounds over 32 grids of 100 by 100: minimums total %lld, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
