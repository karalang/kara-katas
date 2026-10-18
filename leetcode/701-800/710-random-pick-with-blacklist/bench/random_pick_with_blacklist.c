// LeetCode #710: Random Pick with Blacklist -- the r-th allowed number,
// by binary search.
// Benchmark mirror of the Kara rank arm: sort the blacklist; the r-th
// allowed number is r + i, i the first index with more than r allowed
// numbers below its blacklisted number.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t random_below(int64_t *seed, int64_t bound) {
    int64_t hi = next_random(seed);
    int64_t lo = next_random(seed);
    return (hi * 32768 + lo) % bound;
}

typedef struct {
    int64_t bound;
    int64_t *black;
    int64_t len;
    int64_t seed;
} Solution;

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static Solution solution_new(int64_t n, const int64_t *blacklist,
                             int64_t len, int64_t seed) {
    Solution s;
    s.black = malloc(len * sizeof(int64_t));
    memcpy(s.black, blacklist, len * sizeof(int64_t));
    qsort(s.black, len, sizeof(int64_t), cmp);
    s.len = len;
    s.bound = n - len;
    s.seed = seed;
    return s;
}

static int64_t pick_from(const Solution *s, int64_t r) {
    int64_t lo = 0, hi = s->len;
    while (lo < hi) {
        int64_t mid = (lo + hi) / 2;
        if (s->black[mid] - mid > r) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return r + lo;
}

static int64_t pick(Solution *s) {
    int64_t r = random_below(&s->seed, s->bound);
    return pick_from(s, r);
}

int main(void) {
    int64_t n = 1000000000;
    int64_t seed = 710;
    enum { LEN = 100000 };
    int64_t *blacklist = malloc(LEN * sizeof(int64_t));
    for (int64_t i = 0; i < LEN; i++) {
        blacklist[i] = i * 10000 + random_below(&seed, 10000);
    }
    for (int64_t i = LEN - 1; i > 0; i--) {
        int64_t j = random_below(&seed, i + 1);
        int64_t t = blacklist[i];
        blacklist[i] = blacklist[j];
        blacklist[j] = t;
    }
    int64_t sum = 0;
    for (int64_t round = 0; round < 5; round++) {
        Solution s = solution_new(n, blacklist, LEN, 1 + round);
        for (int k = 0; k < 1000000; k++) {
            sum += pick(&s);
        }
        free(s.black);
    }
    free(blacklist);
    printf("5 rounds of 1000000 picks, 100000 of 1000000000 blacklisted: sum %lld\n", (long long)sum);
    return 0;
}
