// Benchmark: LeetCode #986 Interval List Intersections -- the ★ arm, two pointers,
// on pairs of LeetCode's largest lists, 1000 intervals each.
// Mirrors interval_intersection.kara, .rs, .py and go-seq/.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t lo, hi;
} Interval;

typedef struct {
    Interval *items;
    int64_t len, cap;
} List;

static void push(List *l, int64_t lo, int64_t hi) {
    if (l->len == l->cap) {
        l->cap = l->cap ? 2 * l->cap : 4;
        l->items = realloc(l->items, sizeof(Interval) * l->cap);
    }
    l->items[l->len].lo = lo;
    l->items[l->len].hi = hi;
    l->len++;
}

// The answer in a fresh list, which the caller frees.
static List interval_intersection(const List *first, const List *second) {
    List out = {0};
    int64_t i = 0, j = 0;
    while (i < first->len && j < second->len) {
        Interval a = first->items[i], b = second->items[j];
        int64_t lo = a.lo > b.lo ? a.lo : b.lo;
        int64_t hi = a.hi < b.hi ? a.hi : b.hi;
        if (lo <= hi) push(&out, lo, hi);
        if (a.hi < b.hi) {
            i++;
        } else {
            j++;
        }
    }
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t wide_random(int64_t *seed) {
    int64_t high = next_random(seed);
    return high * 32768 + next_random(seed);
}

static List random_list(int64_t *seed) {
    List out = {0};
    int64_t pos = wide_random(seed) % 499999;
    for (int k = 0; k < 1000; k++) {
        int64_t start = pos;
        int64_t end = start + 1 + wide_random(seed) % 499999;
        push(&out, start, end);
        pos = end + 1 + wide_random(seed) % 499999;
    }
    return out;
}

int main(void) {
    int64_t rounds = 1000;
    int64_t seed = 986;
    List lists[21];
    for (int k = 0; k < 21; k++) lists[k] = random_list(&seed);
    int64_t found = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int i = 0; i < 20; i++) {
            int k = (int)((r + i) % 20);
            List answer = interval_intersection(&lists[k], &lists[k + 1]);
            found += answer.len;
            Interval m = answer.items[answer.len / 2];
            check = (check * 31 + answer.len + m.lo % 1000 + m.hi % 1000) % 1000000007;
            free(answer.items);
        }
    }
    printf("%lld rounds over 20 pairs of 1000 intervals: %lld intersections, checksum %lld\n",
           (long long)rounds, (long long)found, (long long)check);
    return 0;
}
