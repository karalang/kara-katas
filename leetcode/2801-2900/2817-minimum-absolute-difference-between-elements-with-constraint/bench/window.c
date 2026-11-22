// LeetCode #2817: Minimum Absolute Difference Between Elements With
// Constraint -- the bench in C: the ★ arm over 10 arrays of 10^5
// distinct numbers up to 10^9, shuffled, x from 0 to 10^5 - 1, all drawn
// first, then each answered 3 times. C has no ordered set, so the window
// is an array kept in order, each number put in its place by a binary
// search and `memmove`, as Python's `bisect.insort` does.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define COUNT 10
#define N 100000

static int64_t seed = 2817;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static int64_t behind[N];

static int64_t first_at_least(int64_t len, int64_t v) {
    int64_t lo = 0, hi = len;
    while (lo < hi) {
        int64_t mid = (lo + hi) / 2;
        if (behind[mid] < v)
            lo = mid + 1;
        else
            hi = mid;
    }
    return lo;
}

static int64_t min_absolute_difference(const int64_t *nums, int64_t n, int64_t x) {
    int64_t len = 0, best = INT64_MAX;
    for (int64_t i = x; i < n; i++) {
        int64_t w = nums[i - x];
        int64_t at = first_at_least(len, w);
        memmove(&behind[at + 1], &behind[at], sizeof(int64_t) * (len - at));
        behind[at] = w;
        len++;
        int64_t v = nums[i];
        int64_t k = first_at_least(len, v);
        if (k < len && behind[k] - v < best) best = behind[k] - v;
        if (k > 0 && v - behind[k - 1] < best) best = v - behind[k - 1];
        if (best == 0) break;
    }
    return best;
}

static int64_t cases[COUNT][N];
static int64_t xs[COUNT];

int main(void) {
    int rounds = 3;
    for (int c = 0; c < COUNT; c++) {
        for (int64_t i = 0; i < N; i++) cases[c][i] = i * 10000 + wide() % 10000 + 1;
        for (int64_t i = N - 1; i >= 1; i--) {
            int64_t j = wide() % (i + 1);
            int64_t t = cases[c][i];
            cases[c][i] = cases[c][j];
            cases[c][j] = t;
        }
        xs[c] = wide() % N;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++)
        for (int c = 0; c < COUNT; c++) {
            int64_t a = min_absolute_difference(cases[c], N, xs[c]);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    printf("%d arrays of %d, %d rounds: differences sum to %lld, checksum %lld\n", COUNT, N, rounds, (long long)total, (long long)check);
    return 0;
}
