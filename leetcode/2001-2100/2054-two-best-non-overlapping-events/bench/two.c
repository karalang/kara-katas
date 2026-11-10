// LeetCode #2054: Two Best Non-Overlapping Events -- C mirror of the ★
// arm's benchmark (two.kara): the same 50 sets of 100000 events, sorted
// by (start, end, value) with `qsort`, the best value from each event on,
// and a binary search for each event's first later start.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t seed = 2054;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t hi = next_random();
    return hi * 32768 + next_random();
}

typedef struct {
    int64_t start, end, value;
} Event;

static int by_start(const void *a, const void *b) {
    const Event *x = a, *y = b;
    if (x->start != y->start) return x->start < y->start ? -1 : 1;
    if (x->end != y->end) return x->end < y->end ? -1 : 1;
    if (x->value != y->value) return x->value < y->value ? -1 : 1;
    return 0;
}

static int64_t max_two_events(const Event *given, int64_t n) {
    Event *events = malloc(n * sizeof(Event));
    memcpy(events, given, n * sizeof(Event));
    qsort(events, n, sizeof(Event), by_start);
    int64_t *best_from = calloc(n + 1, sizeof(int64_t));
    for (int64_t i = n - 1; i >= 0; i--) {
        int64_t v = events[i].value;
        best_from[i] = best_from[i + 1] > v ? best_from[i + 1] : v;
    }
    int64_t best = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t lo = 0, hi = n;
        while (lo < hi) {
            int64_t mid = lo + (hi - lo) / 2;
            if (events[mid].start <= events[i].end) lo = mid + 1;
            else hi = mid;
        }
        int64_t sum = events[i].value + best_from[lo];
        if (sum > best) best = sum;
    }
    free(best_from);
    free(events);
    return best;
}

int main(void) {
    static const int64_t longests[4] = {1000, 1000000, 100000000, 500000000};
    int64_t total = 0, check = 0;
    Event *events = malloc(100000 * sizeof(Event));
    for (int t = 0; t < 50; t++) {
        int64_t longest = longests[t % 4];
        int64_t span = 1000000000 - longest;
        for (int i = 0; i < 100000; i++) {
            int64_t start = wide() % span + 1;
            int64_t end = start + wide() % longest;
            int64_t value = wide() % 1000000 + 1;
            events[i] = (Event){start, end, value};
        }
        int64_t best = max_two_events(events, 100000);
        total += best;
        check = (check * 31 + best) % 1000000007;
    }
    free(events);
    printf("50 sets: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
