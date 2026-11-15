// benchmark's C mirror of dig.kara (LeetCode #2201, the ★ arm): the dug
// cells in a set, each as r * n + c. C has no set, so it is an
// open-addressing table with a multiplicative hash, grown from 16 by
// doubling; Kāra's Set hashes with SipHash-1-3.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *keys;
    int64_t cap, len;
} set_t;

static void set_init(set_t *s, int64_t cap) {
    s->cap = cap;
    s->len = 0;
    s->keys = malloc(sizeof(int64_t) * (size_t)cap);
    memset(s->keys, 0xff, sizeof(int64_t) * (size_t)cap);
}

static int64_t slot(const set_t *s, int64_t key) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ULL;
    int64_t i = (int64_t)(h >> 20) & (s->cap - 1);
    while (s->keys[i] != -1 && s->keys[i] != key) i = (i + 1) & (s->cap - 1);
    return i;
}

static int set_has(const set_t *s, int64_t key) { return s->keys[slot(s, key)] == key; }

static void set_add(set_t *s, int64_t key);

static void set_grow(set_t *s) {
    set_t bigger;
    set_init(&bigger, s->cap * 2);
    for (int64_t i = 0; i < s->cap; i++)
        if (s->keys[i] != -1) set_add(&bigger, s->keys[i]);
    free(s->keys);
    *s = bigger;
}

static void set_add(set_t *s, int64_t key) {
    if ((s->len + 1) * 2 > s->cap) set_grow(s);
    int64_t i = slot(s, key);
    if (s->keys[i] != key) {
        s->keys[i] = key;
        s->len++;
    }
}

static int64_t dig_artifacts(int64_t n, const int64_t (*artifacts)[4], int64_t na, const int64_t (*dig)[2], int64_t nd) {
    set_t dug;
    set_init(&dug, 16);
    for (int64_t i = 0; i < nd; i++) set_add(&dug, dig[i][0] * n + dig[i][1]);
    int64_t count = 0;
    for (int64_t k = 0; k < na; k++) {
        const int64_t *a = artifacts[k];
        int whole = 1;
        for (int64_t r = a[0]; r <= a[2]; r++)
            for (int64_t c = a[1]; c <= a[3]; c++)
                if (!set_has(&dug, r * n + c)) whole = 0;
        if (whole) count++;
    }
    free(dug.keys);
    return count;
}

static int64_t seed = 2201;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t hi = next_random();
    return hi * 32768 + next_random();
}

typedef struct {
    int64_t (*artifacts)[4];
    int64_t na;
    int64_t (*dig)[2];
    int64_t nd;
} site_t;

static site_t site(int64_t n, int64_t tries, int64_t digs) {
    static const int64_t shapes[8][2] = {{1, 1}, {1, 2}, {2, 1}, {2, 2}, {1, 3}, {3, 1}, {1, 4}, {4, 1}};
    char *taken = calloc((size_t)(n * n), 1);
    site_t s;
    s.artifacts = malloc(sizeof(int64_t[4]) * (size_t)tries);
    s.na = 0;
    for (int64_t t = 0; t < tries; t++) {
        int64_t sh = next_random() % 8;
        int64_t h = shapes[sh][0], w = shapes[sh][1];
        int64_t r = wide_random() % (n - h + 1);
        int64_t c = wide_random() % (n - w + 1);
        int free_ = 1;
        for (int64_t i = r; i < r + h; i++)
            for (int64_t j = c; j < c + w; j++)
                if (taken[i * n + j]) free_ = 0;
        if (free_) {
            for (int64_t i = r; i < r + h; i++)
                for (int64_t j = c; j < c + w; j++) taken[i * n + j] = 1;
            int64_t *a = s.artifacts[s.na++];
            a[0] = r;
            a[1] = c;
            a[2] = r + h - 1;
            a[3] = c + w - 1;
        }
    }
    char *dug = calloc((size_t)(n * n), 1);
    s.dig = malloc(sizeof(int64_t[2]) * (size_t)digs);
    s.nd = 0;
    while (s.nd < digs) {
        int64_t cell = wide_random() % (n * n);
        if (!dug[cell]) {
            dug[cell] = 1;
            s.dig[s.nd][0] = cell / n;
            s.dig[s.nd][1] = cell % n;
            s.nd++;
        }
    }
    free(taken);
    free(dug);
    return s;
}

int main(void) {
    site_t sites[8];
    for (int i = 0; i < 8; i++) sites[i] = site(1000, 20000, 300000);
    int64_t check = 0;
    for (int p = 0; p < 10; p++)
        for (int i = 0; i < 8; i++) {
            int64_t count = dig_artifacts(1000, (const int64_t (*)[4])sites[i].artifacts, sites[i].na,
                                          (const int64_t (*)[2])sites[i].dig, sites[i].nd);
            check = (check * 31 + count + sites[i].na) % 1000000007;
        }
    printf("10 passes over 8 sites: checksum %lld\n", (long long)check);
    return 0;
}
