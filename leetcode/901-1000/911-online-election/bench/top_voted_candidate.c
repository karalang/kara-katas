// LeetCode #911: Online Election -- bench program, C.
//
// The leader after every vote, and a binary search for the time, on one
// election of 1,000,000 votes among 1,000 people, built once. Each query
// asks for the leader at a random time and folds the answer into a
// checksum; 2,000,000 queries.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t n;
    int64_t *times;
    int64_t *leaders;
} TopVotedCandidate;

static TopVotedCandidate top_voted_candidate_new(const int64_t *persons, const int64_t *times, int64_t n) {
    TopVotedCandidate e;
    e.n = n;
    int64_t *count = calloc(n, sizeof(int64_t));
    e.leaders = malloc(sizeof(int64_t) * n);
    e.times = malloc(sizeof(int64_t) * n);
    memcpy(e.times, times, sizeof(int64_t) * n);
    int64_t leader = persons[0];
    for (int64_t i = 0; i < n; i++) {
        int64_t p = persons[i];
        count[p] += 1;
        if (count[p] >= count[leader]) leader = p;
        e.leaders[i] = leader;
    }
    free(count);
    return e;
}

static int64_t top_voted_candidate_q(const TopVotedCandidate *e, int64_t t) {
    int64_t lo = 0, hi = e->n;
    while (hi - lo > 1) {
        int64_t mid = (lo + hi) / 2;
        if (e->times[mid] <= t)
            lo = mid;
        else
            hi = mid;
    }
    return e->leaders[lo];
}

static int64_t seed = 911;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t n = 1000000;
    int64_t queries = 2000000;
    int64_t *persons = malloc(sizeof(int64_t) * n);
    int64_t *times = malloc(sizeof(int64_t) * n);
    int64_t at = 0;
    for (int64_t i = 0; i < n; i++) {
        persons[i] = next_random() % 1000;
        times[i] = at;
        at += 1 + next_random() % 1000;
    }
    TopVotedCandidate e = top_voted_candidate_new(persons, times, n);
    int64_t check = 0;
    for (int64_t j = 0; j < queries; j++) {
        int64_t high = next_random();
        int64_t t = (high * 32768 + next_random()) % at;
        check = (check * 31 + top_voted_candidate_q(&e, t)) % 1000000007;
    }
    printf("%lld votes, %lld queries: checksum %lld\n", (long long)n, (long long)queries, (long long)check);
    free(persons);
    free(times);
    free(e.times);
    free(e.leaders);
    return 0;
}
