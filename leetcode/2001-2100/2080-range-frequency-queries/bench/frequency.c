// LeetCode #2080: Range Frequency Queries -- C mirror of the ★ arm's
// benchmark (frequency.kara): 10 arrays of 10^5 values, each built into an
// open-addressing table of every value's places once and then asked
// 1000000 queries, each a pair of binary searches.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 2080;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct {
    int64_t key;
    int64_t *at;
    int64_t len, cap;
    int used;
} Slot;

typedef struct {
    Slot *slots;
    uint64_t mask;
} Table;

static uint64_t hash(int64_t k) {
    uint64_t x = (uint64_t)k * 0x9E3779B97F4A7C15ULL;
    return x ^ (x >> 29);
}

static Slot *find(Table *t, int64_t key, int insert) {
    uint64_t i = hash(key) & t->mask;
    for (;;) {
        Slot *s = &t->slots[i];
        if (!s->used) {
            if (!insert) return NULL;
            s->used = 1;
            s->key = key;
            return s;
        }
        if (s->key == key) return s;
        i = (i + 1) & t->mask;
    }
}

static void build(Table *t, const int64_t *arr, int64_t n) {
    uint64_t size = 1;
    while (size < 2 * (uint64_t)n) size <<= 1;
    t->slots = calloc(size, sizeof(Slot));
    t->mask = size - 1;
    for (int64_t i = 0; i < n; i++) {
        Slot *s = find(t, arr[i], 1);
        if (s->len == s->cap) {
            s->cap = s->cap ? 2 * s->cap : 4;
            s->at = realloc(s->at, s->cap * sizeof(int64_t));
        }
        s->at[s->len++] = i;
    }
}

static void release(Table *t) {
    for (uint64_t i = 0; i <= t->mask; i++) free(t->slots[i].at);
    free(t->slots);
}

// the first place at least x
static int64_t first_at_least(const int64_t *at, int64_t len, int64_t x) {
    int64_t lo = 0, hi = len;
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (at[mid] < x) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

static int64_t query(Table *t, int64_t left, int64_t right, int64_t value) {
    Slot *s = find(t, value, 0);
    if (!s) return 0;
    return first_at_least(s->at, s->len, right + 1) - first_at_least(s->at, s->len, left);
}

int main(void) {
    const int64_t n = 100000;
    const int64_t tops[3] = {100, 1000, 10000};
    int64_t total = 0, check = 0;
    int64_t *arr = malloc(n * sizeof(int64_t));
    for (int t = 0; t < 10; t++) {
        int64_t top = tops[t % 3];
        for (int64_t i = 0; i < n; i++) arr[i] = next_random() % top + 1;
        Table index;
        build(&index, arr, n);
        for (int k = 0; k < 1000000; k++) {
            int64_t a = next_random() * 32768;
            a = (a + next_random()) % n;
            int64_t b = next_random() * 32768;
            b = (b + next_random()) % n;
            int64_t value;
            if (next_random() % 2 == 0) {
                int64_t p = next_random() * 32768;
                p = (p + next_random()) % n;
                value = arr[p];
            } else {
                value = next_random() % (top + 1) + 1;
            }
            int64_t c = query(&index, a < b ? a : b, a < b ? b : a, value);
            total += c;
            check = (check * 31 + c) % 1000000007;
        }
        release(&index);
    }
    free(arr);
    printf("10000000 queries: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
