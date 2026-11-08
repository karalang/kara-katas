// LeetCode #2007: Find Original Array From Doubled Array -- the ★ arm's
// benchmark, a mirror of doubled.kara. The counts and the answer are
// allocated per call, as the Kāra program's are; the answer grows by
// doubling, as a `Vec` does.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t *data; int64_t len, cap; } Vec;

static void push(Vec *v, int64_t x) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->data = realloc(v->data, v->cap * sizeof(int64_t));
    }
    v->data[v->len++] = x;
}

static Vec find_original_array(const int64_t *changed, int64_t n) {
    Vec original = {0, 0, 0};
    if (n % 2 == 1) return original;
    int64_t top = changed[0];
    for (int64_t i = 1; i < n; i++) if (changed[i] > top) top = changed[i];
    int64_t *count = calloc(top + 1, sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) count[changed[i]]++;
    if (count[0] % 2 == 1) { free(count); return original; }
    for (int64_t i = 0; i < count[0] / 2; i++) push(&original, 0);
    for (int64_t v = 1; v <= top; v++) {
        int64_t c = count[v];
        if (c == 0) continue;
        if (2 * v > top || count[2 * v] < c) {
            free(count);
            free(original.data);
            return (Vec){0, 0, 0};
        }
        count[2 * v] -= c;
        for (int64_t i = 0; i < c; i++) push(&original, v);
    }
    free(count);
    return original;
}

static int64_t seed = 2007;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static int64_t arrays[2000][1000];
    for (int a = 0; a < 2000; a++) {
        int64_t *changed = arrays[a];
        for (int i = 0; i < 500; i++) {
            int64_t x = next_random() % 5001;
            changed[2 * i] = x;
            changed[2 * i + 1] = 2 * x;
        }
        for (int64_t i = 999; i >= 1; i--) {
            int64_t j = next_random() % (i + 1);
            int64_t t = changed[i]; changed[i] = changed[j]; changed[j] = t;
        }
        if (next_random() % 3 == 0) {
            int64_t i = next_random() % 1000;
            changed[i] += 1;
        }
    }
    int64_t calls = 0, sum = 0, check = 0;
    for (int r = 0; r < 25; r++) {
        for (int a = 0; a < 2000; a++) {
            Vec original = find_original_array(arrays[a], 1000);
            int64_t total = original.len;
            for (int64_t i = 0; i < original.len; i++) total += original.data[i];
            free(original.data);
            calls++;
            sum += total;
            check = (check * 31 + total) % 1000000007;
        }
    }
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    return 0;
}
