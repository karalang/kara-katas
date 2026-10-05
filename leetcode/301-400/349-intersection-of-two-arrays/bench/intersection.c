/* Benchmark workload for LeetCode #349 — C mirror of intersection.kara.
 *
 * C has no standard hash set, so one is hand-rolled to the runtime Set's
 * shape: allocated per call and freed on the way out, capacity 16, power of
 * two, linear probing, doubling with a full rehash past a 75% load, and
 * deletion by backward shift. It is NOT a 1,001-slot direct-address table,
 * which would be the bitmap arm, a different algorithm. The hash is one
 * multiply (Fibonacci hashing), cheaper than the SipHash-1-3 that Kara's Set
 * and Rust's HashSet use; that is the one way this mirror is not matched.
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define POOL 1000000
#define LEN 1000
#define PAIRS 20000

typedef struct {
    int64_t *keys;
    uint8_t *used;
    size_t cap, len;
} Set;

static size_t slot_of(int64_t k, size_t mask) {
    return (size_t)(((uint64_t)k * 0x9E3779B97F4A7C15ULL) >> 32) & mask;
}

static void set_init(Set *s) {
    s->cap = 16;
    s->len = 0;
    s->keys = malloc(sizeof(int64_t) * s->cap);
    s->used = calloc(s->cap, 1);
}

static void set_free(Set *s) {
    free(s->keys);
    free(s->used);
}

static void set_insert(Set *s, int64_t k);

static void set_grow(Set *s) {
    Set old = *s;
    s->cap = old.cap * 2;
    s->len = 0;
    s->keys = malloc(sizeof(int64_t) * s->cap);
    s->used = calloc(s->cap, 1);
    for (size_t i = 0; i < old.cap; i++)
        if (old.used[i]) set_insert(s, old.keys[i]);
    set_free(&old);
}

static void set_insert(Set *s, int64_t k) {
    if ((s->len + 1) * 4 > s->cap * 3) set_grow(s);
    size_t mask = s->cap - 1, i = slot_of(k, mask);
    while (s->used[i]) {
        if (s->keys[i] == k) return;
        i = (i + 1) & mask;
    }
    s->used[i] = 1;
    s->keys[i] = k;
    s->len++;
}

static int set_remove(Set *s, int64_t k) {
    size_t mask = s->cap - 1, i = slot_of(k, mask);
    while (s->used[i]) {
        if (s->keys[i] == k) {
            size_t hole = i, j = i;
            for (;;) {
                j = (j + 1) & mask;
                if (!s->used[j]) break;
                size_t home = slot_of(s->keys[j], mask);
                /* move j back into the hole unless its home lies in (hole, j] */
                if ((j > hole && (home <= hole || home > j)) || (j < hole && home <= hole && home > j)) {
                    s->keys[hole] = s->keys[j];
                    hole = j;
                }
            }
            s->used[hole] = 0;
            s->len--;
            return 1;
        }
        i = (i + 1) & mask;
    }
    return 0;
}

static int cmp_i64(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t *intersection(const int64_t *a, const int64_t *b, size_t n, size_t m, size_t *out_len) {
    Set seen;
    set_init(&seen);
    for (size_t k = 0; k < n; k++) set_insert(&seen, a[k]);
    int64_t *out = malloc(sizeof(int64_t) * (m ? m : 1));
    size_t len = 0;
    for (size_t k = 0; k < m; k++)
        if (set_remove(&seen, b[k])) out[len++] = b[k];
    set_free(&seen);
    qsort(out, len, sizeof(int64_t), cmp_i64);
    *out_len = len;
    return out;
}

int main(void) {
    int64_t *pool = malloc(sizeof(int64_t) * POOL);
    int64_t x = 349;
    for (int64_t k = 0; k < POOL; k++) {
        x = (x * 1103515245 + 12345) % 2147483648;
        pool[k] = x / 16 % 1001;
    }

    int64_t sink = 0;
    int64_t *a = malloc(sizeof(int64_t) * LEN), *b = malloc(sizeof(int64_t) * LEN);
    for (int64_t p = 0; p < PAIRS; p++) {
        x = (x * 1103515245 + 12345) % 2147483648;
        int64_t i = x / 16 % (POOL - LEN);
        x = (x * 1103515245 + 12345) % 2147483648;
        int64_t j = x / 16 % (POOL - LEN);
        memcpy(a, pool + i, sizeof(int64_t) * LEN);
        memcpy(b, pool + j, sizeof(int64_t) * LEN);
        size_t rlen;
        int64_t *r = intersection(a, b, LEN, LEN, &rlen);
        int64_t s = 0;
        for (size_t k = 0; k < rlen; k++) s += r[k];
        free(r);
        sink = (sink * 31 + (int64_t)rlen * 1000003 + s) % 1000000007;
    }
    free(a);
    free(b);
    free(pool);
    printf("sink %lld\n", (long long)sink);
    return 0;
}
