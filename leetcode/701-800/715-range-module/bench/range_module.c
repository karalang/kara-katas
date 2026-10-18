// LeetCode #715: Range Module -- a sorted list of disjoint ranges.
// Benchmark mirror of the Kara star arm: parallel sorted arrays of
// starts and ends, a binary search on the ends, and inserts and removals
// that shift the rest.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *starts, *ends;
    int64_t len, cap;
} RangeModule;

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t random_below(int64_t *seed, int64_t bound) {
    int64_t hi = next_random(seed);
    int64_t lo = next_random(seed);
    return (hi * 32768 + lo) % bound;
}

static int64_t first_ending_after(const RangeModule *m, int64_t x) {
    int64_t lo = 0, hi = m->len;
    while (lo < hi) {
        int64_t mid = (lo + hi) / 2;
        if (m->ends[mid] > x) hi = mid; else lo = mid + 1;
    }
    return lo;
}

static void insert_at(RangeModule *m, int64_t i, int64_t s, int64_t e) {
    if (m->len == m->cap) {
        m->cap = m->cap ? 2 * m->cap : 4;
        m->starts = realloc(m->starts, m->cap * sizeof(int64_t));
        m->ends = realloc(m->ends, m->cap * sizeof(int64_t));
    }
    memmove(m->starts + i + 1, m->starts + i, (m->len - i) * sizeof(int64_t));
    memmove(m->ends + i + 1, m->ends + i, (m->len - i) * sizeof(int64_t));
    m->starts[i] = s;
    m->ends[i] = e;
    m->len++;
}

static void remove_at(RangeModule *m, int64_t i) {
    memmove(m->starts + i, m->starts + i + 1, (m->len - i - 1) * sizeof(int64_t));
    memmove(m->ends + i, m->ends + i + 1, (m->len - i - 1) * sizeof(int64_t));
    m->len--;
}

static void add_range(RangeModule *m, int64_t left, int64_t right) {
    int64_t i = first_ending_after(m, left - 1);
    int64_t lo = left, hi = right, j = i;
    while (j < m->len && m->starts[j] <= right) {
        if (m->starts[j] < lo) lo = m->starts[j];
        if (m->ends[j] > hi) hi = m->ends[j];
        j++;
    }
    if (j == i) {
        insert_at(m, i, lo, hi);
    } else {
        m->starts[i] = lo;
        m->ends[i] = hi;
        for (int64_t k = i + 1; k < j; k++) remove_at(m, i + 1);
    }
}

static int query_range(const RangeModule *m, int64_t left, int64_t right) {
    int64_t i = first_ending_after(m, left);
    return i < m->len && m->starts[i] <= left && m->ends[i] >= right;
}

static void remove_range(RangeModule *m, int64_t left, int64_t right) {
    int64_t i = first_ending_after(m, left);
    if (i < m->len && m->starts[i] < left) {
        int64_t end = m->ends[i];
        m->ends[i] = left;
        if (end > right) {
            insert_at(m, i + 1, right, end);
            return;
        }
        i++;
    }
    while (i < m->len && m->starts[i] < right) {
        if (m->ends[i] > right) {
            m->starts[i] = right;
            return;
        }
        remove_at(m, i);
    }
}

enum { LISTS = 10, CALLS = 100000 };

int main(void) {
    int64_t seed = 715;
    static int64_t kinds[LISTS][CALLS], lefts[LISTS][CALLS], rights[LISTS][CALLS];
    for (int l = 0; l < LISTS; l++) {
        for (int c = 0; c < CALLS; c++) {
            kinds[l][c] = next_random(&seed) % 3;
            lefts[l][c] = 1 + random_below(&seed, 10000000);
            rights[l][c] = lefts[l][c] + 1 + random_below(&seed, 10000);
        }
    }
    int64_t held = 0;
    for (int round = 0; round < 10; round++) {
        for (int l = 0; l < LISTS; l++) {
            RangeModule m = {0};
            for (int c = 0; c < CALLS; c++) {
                int64_t kind = kinds[l][c], left = lefts[l][c], right = rights[l][c];
                if (kind == 0) add_range(&m, left, right);
                else if (kind == 1) remove_range(&m, left, right);
                else if (query_range(&m, left, right)) held++;
            }
            free(m.starts);
            free(m.ends);
        }
    }
    printf("10 rounds of 10 lists of 100000 calls: %lld queries held\n", (long long)held);
    return 0;
}
