// Benchmark for #554: C mirror of the ★ arm (count the edges at each
// position); see brick_wall.kara. C has no map, so each call makes a
// fresh open-addressing hash table of position -> count, doubled as it
// fills, as a Map grows.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

typedef struct {
    int64_t *keys, *counts;
    size_t cap, len;
} Table;

static size_t slot_of(const Table *t, int64_t key) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ULL;
    size_t i = (size_t)(h >> 32) & (t->cap - 1);
    while (t->counts[i] != 0 && t->keys[i] != key) i = (i + 1) & (t->cap - 1);
    return i;
}

static void grow(Table *t) {
    Table bigger = {0, 0, t->cap ? t->cap * 2 : 16, 0};
    bigger.keys = malloc(bigger.cap * sizeof(int64_t));
    bigger.counts = calloc(bigger.cap, sizeof(int64_t));
    for (size_t i = 0; i < t->cap; i++) {
        if (t->counts[i] != 0) {
            size_t s = slot_of(&bigger, t->keys[i]);
            bigger.keys[s] = t->keys[i];
            bigger.counts[s] = t->counts[i];
            bigger.len++;
        }
    }
    free(t->keys);
    free(t->counts);
    *t = bigger;
}

static int64_t least_bricks(int64_t **wall, const size_t *lens, size_t rows) {
    Table edges = {0, 0, 0, 0};
    grow(&edges);
    int64_t most = 0;
    for (size_t r = 0; r < rows; r++) {
        int64_t at = 0;
        for (size_t j = 0; j + 1 < lens[r]; j++) {
            at += wall[r][j];
            size_t s = slot_of(&edges, at);
            if (edges.counts[s] == 0) {
                if ((edges.len + 1) * 4 > edges.cap * 3) {
                    grow(&edges);
                    s = slot_of(&edges, at);
                }
                edges.keys[s] = at;
                edges.len++;
            }
            int64_t count = ++edges.counts[s];
            if (count > most) most = count;
        }
    }
    free(edges.keys);
    free(edges.counts);
    return (int64_t)rows - most;
}

typedef struct {
    int64_t **rows;
    size_t *lens;
    size_t n;
} Wall;

int main(void) {
    const int count = 20;
    int64_t seed = 554;
    Wall walls[20];
    long bricks = 0;
    for (int i = 0; i < count; i++) {
        size_t cap = 16, rows = 0;
        int64_t **rs = malloc(cap * sizeof(int64_t *));
        size_t *ls = malloc(cap * sizeof(size_t));
        long n = 0;
        while (n < 19000) {
            size_t rcap = 16, len = 0;
            int64_t *row = malloc(rcap * sizeof(int64_t));
            int64_t left = 1000000;
            while (left > 0) {
                int64_t a = next_random(&seed);
                int64_t b = next_random(&seed);
                int64_t w = 1 + (a * 32768 + b) % 10000;
                if (w > left) w = left;
                if (len == rcap) row = realloc(row, (rcap *= 2) * sizeof(int64_t));
                row[len++] = w;
                left -= w;
            }
            n += (long)len;
            if (rows == cap) {
                cap *= 2;
                rs = realloc(rs, cap * sizeof(int64_t *));
                ls = realloc(ls, cap * sizeof(size_t));
            }
            rs[rows] = row;
            ls[rows] = len;
            rows++;
        }
        bricks += n;
        walls[i] = (Wall){rs, ls, rows};
    }
    int64_t total = 0, checksum = 0;
    for (int round = 0; round < 50; round++) {
        for (int g = 0; g < count; g++) {
            Wall *w = &walls[(round * 7 + g) % count];
            int64_t got = least_bricks(w->rows, w->lens, w->n);
            total += got;
            checksum = (checksum * 31 + got) % 1000000007;
        }
    }
    printf("%d walls, %ld bricks, 50 rounds each: total %lld, checksum %lld\n", count, bricks,
           (long long)total, (long long)checksum);
    return 0;
}
