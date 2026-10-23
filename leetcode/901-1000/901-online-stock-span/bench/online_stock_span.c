// LeetCode #901: Online Stock Span -- bench program, C.
//
// The stack of prices and their spans over 1,000,000 prices built once, a
// random walk between 1 and 10^5 taking steps of -50 to 50. Each round
// gives every price to a fresh spanner, folds the spans into a checksum
// and changes one price.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *prices;
    int64_t *spans;
    int64_t len;
    int64_t cap;
} StockSpanner;

static StockSpanner spanner_new(void) {
    StockSpanner s = {NULL, NULL, 0, 0};
    return s;
}

static void spanner_free(StockSpanner *s) {
    free(s->prices);
    free(s->spans);
}

static int64_t spanner_next(StockSpanner *s, int64_t price) {
    int64_t span = 1;
    while (s->len > 0 && s->prices[s->len - 1] <= price) {
        span += s->spans[s->len - 1];
        s->len -= 1;
    }
    if (s->len == s->cap) {
        s->cap = s->cap == 0 ? 4 : 2 * s->cap;
        s->prices = realloc(s->prices, sizeof(int64_t) * s->cap);
        s->spans = realloc(s->spans, sizeof(int64_t) * s->cap);
    }
    s->prices[s->len] = price;
    s->spans[s->len] = span;
    s->len += 1;
    return span;
}

static int64_t seed = 901;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t days = 1000000;
    int64_t rounds = 50;
    int64_t *prices = malloc(sizeof(int64_t) * days);
    int64_t p = 50000;
    for (int64_t d = 0; d < days; d++) {
        p = p + next_random() % 101 - 50;
        if (p < 1) p = 1;
        if (p > 100000) p = 100000;
        prices[d] = p;
    }
    int64_t check = 0;
    int64_t total = 0;
    for (int64_t round = 0; round < rounds; round++) {
        StockSpanner s = spanner_new();
        for (int64_t d = 0; d < days; d++) {
            int64_t span = spanner_next(&s, prices[d]);
            total += span;
            check = (check * 31 + span) % 1000000007;
        }
        spanner_free(&s);
        prices[round * 7919 % days] = 1 + next_random() % 100000;
    }
    printf("%lld rounds over %lld prices: spans summing to %lld, checksum %lld\n", (long long)rounds,
           (long long)days, (long long)total, (long long)check);
    free(prices);
    return 0;
}
