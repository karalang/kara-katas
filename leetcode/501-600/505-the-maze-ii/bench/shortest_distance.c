// Benchmark for #505 in C: the ★ arm (Dijkstra over the cells the ball
// can stop in); see ../shortest_distance.kara. A binary heap written here
// of (distance, row, column) triples is the smallest-first queue; it and
// the grid of best distances are malloc'd for each call.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100

typedef struct {
    int64_t d, r, c;
} Entry;

static int less(Entry a, Entry b) {
    if (a.d != b.d) return a.d < b.d;
    if (a.r != b.r) return a.r < b.r;
    return a.c < b.c;
}

typedef struct {
    Entry *items;
    int64_t len, cap;
} Heap;

static void heap_push(Heap *h, Entry e) {
    if (h->len == h->cap) {
        h->cap = h->cap ? h->cap * 2 : 16;
        h->items = realloc(h->items, (size_t)h->cap * sizeof(Entry));
    }
    int64_t i = h->len++;
    h->items[i] = e;
    while (i > 0) {
        int64_t p = (i - 1) / 2;
        if (!less(h->items[i], h->items[p])) break;
        Entry t = h->items[i];
        h->items[i] = h->items[p];
        h->items[p] = t;
        i = p;
    }
}

static Entry heap_pop(Heap *h) {
    Entry top = h->items[0];
    h->items[0] = h->items[--h->len];
    int64_t i = 0;
    for (;;) {
        int64_t l = 2 * i + 1, r = l + 1, m = i;
        if (l < h->len && less(h->items[l], h->items[m])) m = l;
        if (r < h->len && less(h->items[r], h->items[m])) m = r;
        if (m == i) break;
        Entry t = h->items[i];
        h->items[i] = h->items[m];
        h->items[m] = t;
        i = m;
    }
    return top;
}

static int64_t shortest_distance(const int64_t *maze, int64_t rows, int64_t cols, const int64_t *start,
                                 const int64_t *destination) {
    int64_t *best = malloc((size_t)(rows * cols) * sizeof(int64_t));
    for (int64_t i = 0; i < rows * cols; i++) best[i] = -1;
    Heap queue = {0};
    heap_push(&queue, (Entry){0, start[0], start[1]});
    static const int64_t moves[4][2] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    int64_t answer = -1;
    while (queue.len > 0) {
        Entry e = heap_pop(&queue);
        int64_t d = e.d, r = e.r, c = e.c;
        if (best[r * cols + c] != -1) continue;
        best[r * cols + c] = d;
        if (r == destination[0] && c == destination[1]) {
            answer = d;
            break;
        }
        for (int k = 0; k < 4; k++) {
            int64_t dr = moves[k][0], dc = moves[k][1];
            int64_t nr = r, nc = c, steps = 0;
            while (nr + dr >= 0 && nr + dr < rows && nc + dc >= 0 && nc + dc < cols &&
                   maze[(nr + dr) * cols + nc + dc] == 0) {
                nr += dr;
                nc += dc;
                steps++;
            }
            if (steps > 0 && best[nr * cols + nc] == -1) heap_push(&queue, (Entry){d + steps, nr, nc});
        }
    }
    free(queue.items);
    free(best);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    // 2,000 mazes of 100 by 100 (the problem's most), a wall in each
    // cell with odds of 1 in 4, with a start and a destination in two
    // different open cells, built once. Then each is solved once.
    const int64_t mazes = 2000;
    int64_t seed = 505;
    int64_t *all = malloc((size_t)(mazes * N * N) * sizeof(int64_t));
    int64_t *starts = malloc((size_t)(mazes * 2) * sizeof(int64_t));
    int64_t *destinations = malloc((size_t)(mazes * 2) * sizeof(int64_t));
    int64_t *open = malloc((size_t)(N * N * 2) * sizeof(int64_t));
    for (int64_t k = 0; k < mazes; k++) {
        int64_t n = 0;
        for (int64_t r = 0; r < N; r++) {
            for (int64_t c = 0; c < N; c++) {
                if (next_random(&seed) % 4 == 0) {
                    all[k * N * N + r * N + c] = 1;
                } else {
                    all[k * N * N + r * N + c] = 0;
                    open[2 * n] = r;
                    open[2 * n + 1] = c;
                    n++;
                }
            }
        }
        int64_t a = next_random(&seed) % n;
        int64_t b = next_random(&seed) % (n - 1);
        if (b >= a) b++;
        starts[2 * k] = open[2 * a];
        starts[2 * k + 1] = open[2 * a + 1];
        destinations[2 * k] = open[2 * b];
        destinations[2 * k + 1] = open[2 * b + 1];
    }
    int64_t reached = 0, total = 0, checksum = 0;
    for (int64_t k = 0; k < mazes; k++) {
        int64_t d = shortest_distance(all + k * N * N, N, N, starts + 2 * k, destinations + 2 * k);
        if (d != -1) {
            reached++;
            total += d;
        }
        checksum = (checksum * 31 + d + 1) % 1000000007;
    }
    printf("%lld mazes of 100 by 100: the destination reached in %lld, distance %lld in all, checksum %lld\n",
           (long long)mazes, (long long)reached, (long long)total, (long long)checksum);
    free(all);
    free(starts);
    free(destinations);
    free(open);
    return 0;
}
