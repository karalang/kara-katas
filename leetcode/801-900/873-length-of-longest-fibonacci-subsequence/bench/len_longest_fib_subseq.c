// LeetCode #873 bench: C mirror of len_longest_fib_subseq.kara (the ★ arm)
// on the same 100 arrays. C has no hash map, so the value index is an
// open-addressing table with linear probing.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *keys;
    int *vals;
    size_t mask;
} Index;

static size_t slot(int64_t key, size_t mask) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ull;
    return (size_t)(h >> 32) & mask;
}

static void index_init(Index *ix, size_t n) {
    size_t cap = 1;
    while (cap < 2 * n) cap <<= 1;
    ix->keys = malloc(cap * sizeof(int64_t));
    ix->vals = malloc(cap * sizeof(int));
    ix->mask = cap - 1;
    for (size_t i = 0; i < cap; i++) ix->keys[i] = -1;
}

static void index_put(Index *ix, int64_t key, int val) {
    size_t s = slot(key, ix->mask);
    while (ix->keys[s] != -1 && ix->keys[s] != key) s = (s + 1) & ix->mask;
    ix->keys[s] = key;
    ix->vals[s] = val;
}

static int index_get(const Index *ix, int64_t key) {
    size_t s = slot(key, ix->mask);
    while (ix->keys[s] != -1) {
        if (ix->keys[s] == key) return ix->vals[s];
        s = (s + 1) & ix->mask;
    }
    return -1;
}

static int64_t len_longest_fib_subseq(const int64_t *arr, int n) {
    Index ix;
    index_init(&ix, (size_t)n);
    for (int i = 0; i < n; i++) index_put(&ix, arr[i], i);
    int64_t *longest = malloc((size_t)n * (size_t)n * sizeof(int64_t));
    for (size_t i = 0; i < (size_t)n * (size_t)n; i++) longest[i] = 2;
    int64_t best = 0;
    for (int k = 0; k < n; k++) {
        for (int j = 0; j < k; j++) {
            int64_t before = arr[k] - arr[j];
            if (before < arr[j]) {
                int i = index_get(&ix, before);
                if (i >= 0) {
                    int64_t v = longest[(size_t)i * n + j] + 1;
                    longest[(size_t)j * n + k] = v;
                    if (v > best) best = v;
                }
            }
        }
    }
    free(longest);
    free(ix.keys);
    free(ix.vals);
    return best;
}

static int64_t seed = 873;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int increasing(int64_t *arr, int n, int64_t gap) {
    int64_t x = 0;
    for (int i = 0; i < n; i++) {
        x += 1 + next_random() % gap;
        arr[i] = x;
    }
    return n;
}

static int64_t big(void) {
    int64_t hi = next_random();
    return (hi * 32768 + next_random()) % 1000000000 + 1;
}

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int scattered(int64_t *arr, int n, int run) {
    int64_t *vals = malloc((size_t)n * sizeof(int64_t));
    int len = 0;
    int64_t a = next_random() % 1000 + 1;
    int64_t b = a + next_random() % 1000 + 1;
    vals[len++] = a;
    vals[len++] = b;
    while (len < run && a + b <= 1000000000) {
        int64_t next = a + b;
        a = b;
        b = next;
        vals[len++] = b;
    }
    while (len < n) vals[len++] = big();
    qsort(vals, (size_t)len, sizeof(int64_t), cmp);
    int out = 0;
    for (int i = 0; i < len; i++)
        if (out == 0 || arr[out - 1] != vals[i]) arr[out++] = vals[i];
    free(vals);
    return out;
}

int main(void) {
    static int64_t arrays[100][1000];
    int lens[100];
    for (int k = 0; k < 100; k++)
        lens[k] = k % 2 == 0 ? increasing(arrays[k], 1000, k % 5 + 2) : scattered(arrays[k], 1000, 10 + k % 30);
    int64_t total = 0, check = 0;
    for (int k = 0; k < 100; k++) {
        int64_t answer = len_longest_fib_subseq(arrays[k], lens[k]);
        total += answer;
        check = (check * 131 + answer) % 1000000007;
    }
    printf("100 arrays of 1000 values: lengths sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
