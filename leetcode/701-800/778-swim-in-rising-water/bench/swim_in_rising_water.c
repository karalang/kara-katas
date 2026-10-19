// Benchmark for #778: Swim in Rising Water -- mirror of the ★ arm
// (Dijkstra on the highest square), with the same workload as the Kāra
// program.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int64_t t, at; } Entry;
typedef struct { Entry *items; int64_t len, cap; } Heap;

static int less(Entry a, Entry b) { return a.t < b.t || (a.t == b.t && a.at < b.at); }

static void heap_push(Heap *h, Entry e) {
    if (h->len == h->cap) {
        h->cap = h->cap ? 2 * h->cap : 4;
        h->items = realloc(h->items, h->cap * sizeof(Entry));
    }
    int64_t i = h->len++;
    while (i > 0) {
        int64_t p = (i - 1) / 2;
        if (!less(e, h->items[p])) break;
        h->items[i] = h->items[p];
        i = p;
    }
    h->items[i] = e;
}

static Entry heap_pop(Heap *h) {
    Entry top = h->items[0];
    Entry last = h->items[--h->len];
    int64_t i = 0;
    for (;;) {
        int64_t c = 2 * i + 1;
        if (c >= h->len) break;
        if (c + 1 < h->len && less(h->items[c + 1], h->items[c])) c++;
        if (!less(h->items[c], last)) break;
        h->items[i] = h->items[c];
        i = c;
    }
    if (h->len > 0) h->items[i] = last;
    return top;
}

static const int64_t DR[4] = {0, 1, 0, -1};
static const int64_t DC[4] = {1, 0, -1, 0};

static int64_t swim_in_water(int64_t **grid, int64_t n) {
    bool *done = calloc(n * n, sizeof(bool));
    Heap queue = {0};
    heap_push(&queue, (Entry){grid[0][0], 0});
    int64_t answer = -1;
    while (queue.len > 0) {
        Entry e = heap_pop(&queue);
        if (done[e.at]) continue;
        done[e.at] = true;
        int64_t r = e.at / n, c = e.at % n;
        if (r == n - 1 && c == n - 1) {
            answer = e.t;
            break;
        }
        for (int d = 0; d < 4; d++) {
            int64_t nr = r + DR[d], nc = c + DC[d];
            if (nr >= 0 && nr < n && nc >= 0 && nc < n && !done[nr * n + nc]) {
                int64_t h = grid[nr][nc];
                heap_push(&queue, (Entry){h > e.t ? h : e.t, nr * n + nc});
            }
        }
    }
    free(queue.items);
    free(done);
    return answer;
}

static int64_t seed = 778;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    enum { COUNT = 64, N = 50 };
    int64_t **grids[COUNT];
    int64_t values[N * N];
    for (int64_t g = 0; g < COUNT; g++) {
        for (int64_t r = 0; r < N; r++)
            for (int64_t c = 0; c < N; c++)
                values[r * N + c] = (g % 4 == 2 && r % 2 == 1) ? r * N + N - 1 - c : r * N + c;
        if (g % 4 < 2) {
            for (int64_t i = N * N - 1; i > 0; i--) {
                int64_t j = next_random() % (i + 1);
                int64_t t = values[i]; values[i] = values[j]; values[j] = t;
            }
        } else {
            for (int k = 0; k < 50; k++) {
                int64_t i = next_random() % (N * N);
                int64_t j = next_random() % (N * N);
                int64_t t = values[i]; values[i] = values[j]; values[j] = t;
            }
        }
        grids[g] = malloc(N * sizeof(int64_t *));
        for (int64_t r = 0; r < N; r++) {
            grids[g][r] = malloc(N * sizeof(int64_t));
            memcpy(grids[g][r], &values[r * N], N * sizeof(int64_t));
        }
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < 3000; round++) {
        int64_t g = (round * 7) % COUNT;
        int64_t answer = swim_in_water(grids[g], N);
        total += answer;
        checksum = (checksum * 31 + answer + g) % 1000000007;
    }
    printf("3000 rounds of 50 x 50 grids: answers sum to %lld, checksum %lld\n", (long long)total, (long long)checksum);
    return 0;
}
