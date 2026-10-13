// Benchmark for #496: C mirror of the ★ arm (a stack and a map); see
// next_greater_element.kara. C has no hash map, so the map is the small
// open-addressing table of #447 (linear probing, doubled at half full,
// a 64-bit mixing hash), fresh for each case as the ★ arm's Map is.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define CASES 10000
#define N2 1000
#define N1 500
#define POOL 10001

typedef struct {
    int64_t *keys;
    int64_t *values;
    uint8_t *used;
    int64_t cap, len;
} Table;

static uint64_t mix(int64_t key) {
    uint64_t x = (uint64_t)key;
    x ^= x >> 33;
    x *= 0xff51afd7ed558ccdULL;
    x ^= x >> 33;
    x *= 0xc4ceb9fe1a85ec53ULL;
    x ^= x >> 33;
    return x;
}

static void table_init(Table *t, int64_t cap) {
    t->cap = cap;
    t->len = 0;
    t->keys = malloc(cap * sizeof(int64_t));
    t->values = malloc(cap * sizeof(int64_t));
    t->used = calloc(cap, 1);
}

static void table_free(Table *t) {
    free(t->keys);
    free(t->values);
    free(t->used);
}

static void table_set(Table *t, int64_t key, int64_t value);

static void table_grow(Table *t) {
    Table bigger;
    table_init(&bigger, t->cap * 2);
    for (int64_t i = 0; i < t->cap; i++) {
        if (t->used[i]) {
            table_set(&bigger, t->keys[i], t->values[i]);
        }
    }
    table_free(t);
    *t = bigger;
}

static void table_set(Table *t, int64_t key, int64_t value) {
    if ((t->len + 1) * 2 > t->cap) {
        table_grow(t);
    }
    uint64_t mask = (uint64_t)t->cap - 1;
    for (uint64_t at = mix(key) & mask;; at = (at + 1) & mask) {
        if (!t->used[at]) {
            t->used[at] = 1;
            t->keys[at] = key;
            t->values[at] = value;
            t->len++;
            return;
        }
        if (t->keys[at] == key) {
            t->values[at] = value;
            return;
        }
    }
}

static int table_get(const Table *t, int64_t key, int64_t *value) {
    uint64_t mask = (uint64_t)t->cap - 1;
    for (uint64_t at = mix(key) & mask; t->used[at]; at = (at + 1) & mask) {
        if (t->keys[at] == key) {
            *value = t->values[at];
            return 1;
        }
    }
    return 0;
}

// Writes the n1 answers to out.
static void next_greater_element(const int64_t *nums1, int64_t n1, const int64_t *nums2, int64_t n2, int64_t *out) {
    Table next;
    table_init(&next, 8);
    int64_t *waiting = malloc(n2 * sizeof(int64_t));
    int64_t top = 0;
    for (int64_t i = 0; i < n2; i++) {
        int64_t x = nums2[i];
        while (top > 0) {
            if (waiting[top - 1] >= x) {
                break;
            }
            table_set(&next, waiting[top - 1], x);
            top--;
        }
        waiting[top++] = x;
    }
    for (int64_t i = 0; i < n1; i++) {
        int64_t g;
        out[i] = table_get(&next, nums1[i], &g) ? g : -1;
    }
    free(waiting);
    table_free(&next);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // 10,000 cases, built once: nums2 is 1,000 distinct numbers from 0
    // to 10,000 (the problem's most), drawn by shuffling the front of a
    // pool of all of them, and nums1 is every other one of them from the
    // end. Then each case is solved once.
    static int64_t all1[CASES][N1];
    static int64_t all2[CASES][N2];
    static int64_t pool[POOL];
    int64_t seed = 496;
    for (int64_t x = 0; x < POOL; x++) {
        pool[x] = x;
    }
    for (int c = 0; c < CASES; c++) {
        for (int64_t i = 0; i < N2; i++) {
            int64_t j = i + next_random(&seed) % (POOL - i);
            int64_t t = pool[i];
            pool[i] = pool[j];
            pool[j] = t;
        }
        for (int i = 0; i < N2; i++) {
            all2[c][i] = pool[i];
        }
        int n = 0;
        for (int k = N2 - 1; k >= 0; k -= 2) {
            all1[c][n++] = all2[c][k];
        }
    }
    int64_t found = 0, checksum = 0;
    static int64_t answers[N1];
    for (int c = 0; c < CASES; c++) {
        next_greater_element(all1[c], N1, all2[c], N2, answers);
        for (int i = 0; i < N1; i++) {
            if (answers[i] >= 0) {
                found++;
            }
            checksum = (checksum * 31 + answers[i] + 2) % 1000000007;
        }
    }
    printf("%d cases of 1000 and 500: %lld with a greater number, checksum %lld\n", CASES, (long long)found, (long long)checksum);
    return 0;
}
