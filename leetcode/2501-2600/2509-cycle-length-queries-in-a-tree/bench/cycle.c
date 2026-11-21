// LeetCode #2509: Cycle Length Queries in a Tree -- C mirror of the
// benchmark (cycle.kara): the same queries, passes and checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 100000

static void cycle_length_queries(int64_t n, const int64_t (*queries)[2], int64_t count, int64_t *answer) {
    (void)n;
    for (int64_t i = 0; i < count; i++) {
        int64_t a = queries[i][0], b = queries[i][1], length = 1;
        while (a != b) {
            if (a > b) a /= 2;
            else b /= 2;
            length++;
        }
        answer[i] = length;
    }
}

static int64_t seed = 2509;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t below(int64_t top) {
    int64_t hi = next_random();
    return (hi * 32768 + next_random()) % top;
}

int main(void) {
    const int64_t size = (1LL << 30) - 1;
    int64_t (*queries)[2] = malloc(COUNT * sizeof *queries);
    int64_t *answer = malloc(COUNT * sizeof *answer);
    int64_t count = 0;
    while (count < COUNT) {
        int64_t a = below(size) + 1;
        int64_t b = below(size) + 1;
        if (a != b) {
            queries[count][0] = a;
            queries[count][1] = b;
            count++;
        }
    }
    const int64_t passes = 34;
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++) {
        int64_t at = check % COUNT;
        int64_t kept = queries[at][1];
        int64_t b = (check + p) % size + 1;
        if (b == queries[at][0]) b = b % size + 1;
        queries[at][1] = b;
        cycle_length_queries(30, (const int64_t (*)[2])queries, COUNT, answer);
        for (int64_t i = 0; i < COUNT; i++) check = (check * 31 + answer[i] + p) % 1000000007;
        queries[at][1] = kept;
    }
    printf("%lld passes over 10^5 queries on 30 levels: checksum %lld\n", (long long)passes, (long long)check);
    free(queries);
    free(answer);
    return 0;
}
