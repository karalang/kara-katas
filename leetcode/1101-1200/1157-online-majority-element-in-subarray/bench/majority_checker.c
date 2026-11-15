// LeetCode #1157 bench: the ★ arm's vote tree and sorted places, the same
// workload as majority_checker.kara. The places of each value are one
// array cut by offsets.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t value, votes; } Vote;
typedef struct {
    int64_t size;
    Vote *tree;
    int64_t *start;  // places of value v: places[start[v] .. start[v + 1])
    int64_t *places;
} Checker;

static Vote vote(Vote a, Vote b) {
    if (a.value == b.value) return (Vote){a.value, a.votes + b.votes};
    if (a.votes >= b.votes) return (Vote){a.value, a.votes - b.votes};
    return (Vote){b.value, b.votes - a.votes};
}

static Checker checker_new(const int32_t *arr, int64_t n) {
    Checker c;
    c.size = 1;
    while (c.size < n) c.size *= 2;
    c.tree = calloc(2 * c.size, sizeof(Vote));
    c.start = calloc(20002, sizeof(int64_t));
    c.places = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        c.tree[c.size + i] = (Vote){arr[i], 1};
        c.start[arr[i] + 1]++;
    }
    for (int64_t v = 1; v <= 20001; v++) c.start[v] += c.start[v - 1];
    int64_t *fill = malloc(20001 * sizeof(int64_t));
    for (int64_t v = 0; v < 20001; v++) fill[v] = c.start[v];
    for (int64_t i = 0; i < n; i++) c.places[fill[arr[i]]++] = i;
    free(fill);
    for (int64_t i = c.size - 1; i >= 1; i--) c.tree[i] = vote(c.tree[2 * i], c.tree[2 * i + 1]);
    return c;
}

// The first place in p[lo..hi) not below x, searched as Rust's and
// Kāra's `partition_point` search: the span halved by a select marked
// unpredictable, as Rust's library marks it, and one last comparison.
// Without the mark clang turns the select into a branch that mispredicts
// about half the time, which costs this bench about 0.35 s.
static int64_t lower(const int64_t *p, int64_t lo, int64_t hi, int64_t x) {
    int64_t size = hi - lo;
    if (size == 0) return lo;
    const int64_t *base = p + lo;
    while (size > 1) {
        int64_t half = size / 2;
        base = __builtin_unpredictable(base[half] < x) ? base + half : base;
        size -= half;
    }
    return (base - p) + (*base < x);
}

static int64_t query(const Checker *c, int64_t left, int64_t right, int64_t threshold) {
    int64_t lo = left + c->size, hi = right + c->size + 1;
    Vote won = {0, 0};
    while (lo < hi) {
        if (lo % 2 == 1) won = vote(won, c->tree[lo++]);
        if (hi % 2 == 1) won = vote(won, c->tree[--hi]);
        lo /= 2;
        hi /= 2;
    }
    int64_t a = c->start[won.value], b = c->start[won.value + 1];
    int64_t count = lower(c->places, a, b, right + 1) - lower(c->places, a, b, left);
    return count >= threshold ? won.value : -1;
}

static int64_t seed = 1157;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t passes = 100;
    Checker checkers[4];
    int64_t (*queries)[3] = malloc(4 * 10000 * sizeof *queries);
    int32_t *arr = malloc(20000 * sizeof(int32_t));
    for (int kind = 0; kind < 4; kind++) {
        int64_t v = 1 + next_random() % 20000;
        for (int i = 0; i < 20000; i++) {
            int64_t x;
            if (kind == 0) x = 1 + next_random() % 2;
            else if (kind == 2) x = 1 + next_random() % 20000;
            else if (next_random() % 100 < (kind == 1 ? 67 : 50)) x = v;
            else x = 1 + next_random() % 20000;
            arr[i] = (int32_t)x;
        }
        checkers[kind] = checker_new(arr, 20000);
        for (int q = 0; q < 10000; q++) {
            int64_t a = next_random() % 20000, b = next_random() % 20000;
            int64_t left = a < b ? a : b, right = a < b ? b : a;
            int64_t least = (right - left + 1) / 2 + 1;
            int64_t *Q = queries[kind * 10000 + q];
            Q[0] = left;
            Q[1] = right;
            Q[2] = least + next_random() % (right - left + 2 - least);
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++)
        for (int k = 0; k < 4; k++)
            for (int q = 0; q < 10000; q++) {
                int64_t *Q = queries[k * 10000 + q];
                check = (check * 31 + query(&checkers[k], Q[0], Q[1], Q[2]) + p + 1) % 1000000007;
            }
    printf("%lld passes over 4 arrays of 20000 values, 10000 queries each: checksum %lld\n", (long long)passes, (long long)check);
    return 0;
}
