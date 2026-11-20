// LeetCode #1751: Maximum Number of Events That Can Be Attended II -- the
// bench (events.kara in C): sorted by end, one layer of k at a time.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { COUNT = 10, ROUNDS = 5, N = 100000, K = 10 };

typedef struct { int32_t start, end, value; } Event;

static int by_end(const void *a, const void *b) {
    const Event *x = a, *y = b;
    if (x->end != y->end) return x->end < y->end ? -1 : 1;
    if (x->start != y->start) return x->start < y->start ? -1 : 1;
    return (x->value > y->value) - (x->value < y->value);
}

static int32_t max32(int32_t a, int32_t b) { return a > b ? a : b; }

static int32_t max_value(const Event *given, int64_t n, int32_t k) {
    Event *events = malloc(n * sizeof(Event));
    memcpy(events, given, n * sizeof(Event));
    qsort(events, n, sizeof(Event), by_end);
    int64_t *before = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        int64_t lo = 0, hi = n;
        while (lo < hi) {
            int64_t mid = (lo + hi) / 2;
            if (events[mid].end < events[i].start) lo = mid + 1;
            else hi = mid;
        }
        before[i] = lo;
    }
    int32_t *previous = calloc(n + 1, sizeof(int32_t));
    for (int32_t layer = 0; layer < k; layer++) {
        int32_t *current = calloc(n + 1, sizeof(int32_t));
        for (int64_t i = 0; i < n; i++)
            current[i + 1] = max32(current[i], previous[before[i]] + events[i].value);
        free(previous);
        previous = current;
    }
    int32_t answer = previous[n];
    free(previous);
    free(before);
    free(events);
    return answer;
}

static int64_t seed = 1751;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    static Event problems[COUNT][N];
    for (int c = 0; c < COUNT; c++) {
        for (int64_t i = 0; i < N; i++) {
            int64_t start = wide() % 1000000000 + 1;
            int64_t end = start + wide() % 100000000;
            if (end > 1000000000) end = 1000000000;
            int64_t value = wide() % 1000000 + 1;
            problems[c][i] = (Event){(int32_t)start, (int32_t)end, (int32_t)value};
        }
    }
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t answer = max_value(problems[c], N, K);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d problems of %d events, k = %d, %d rounds: values add to %lld, checksum %lld\n", COUNT, N, K, ROUNDS, (long long)sum, (long long)check);
    return 0;
}
