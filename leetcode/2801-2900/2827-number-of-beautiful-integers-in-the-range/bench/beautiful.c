// LeetCode #2827: Number of Beautiful Integers in the Range -- the
// bench's C mirror of the ★ arm: a digit DP up to high less one up to
// low - 1, the free started states memoized in a flat array.

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

static long long walk(const int *digits, int n, int pos, int diff, int rem, bool tight, bool started, int k,
                      long long *memo) {
    if (pos == n) return started && diff == 0 && rem == 0 ? 1 : 0;
    int key = (pos * (2 * n + 1) + diff + n) * k + rem;
    if (!tight && started && memo[key] >= 0) return memo[key];
    int top = tight ? digits[pos] : 9;
    long long total = 0;
    for (int d = 0; d <= top; d++) {
        bool now = started || d > 0;
        int next_diff = now ? diff + (d % 2 == 0 ? 1 : -1) : 0;
        total += walk(digits, n, pos + 1, next_diff, (rem * 10 + d) % k, tight && d == top, now, k, memo);
    }
    if (!tight && started) memo[key] = total;
    return total;
}

static long long count_upto(long long x, int k) {
    if (x <= 0) return 0;
    char text[24];
    int n = snprintf(text, sizeof text, "%lld", x);
    int digits[24];
    for (int i = 0; i < n; i++) digits[i] = text[i] - '0';
    int size = n * (2 * n + 1) * k;
    long long *memo = malloc(size * sizeof *memo);
    for (int i = 0; i < size; i++) memo[i] = -1;
    long long total = walk(digits, n, 0, 0, 0, true, false, k, memo);
    free(memo);
    return total;
}

static long long seed = 2827;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long wide(void) {
    long long a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    enum { COUNT = 2000, ROUNDS = 5 };
    static long long lows[COUNT], highs[COUNT];
    static int ks[COUNT];
    for (int c = 0; c < COUNT; c++) {
        long long a = wide() % 1000000000 + 1, b = wide() % 1000000000 + 1;
        lows[c] = a < b ? a : b;
        highs[c] = a < b ? b : a;
        ks[c] = (int)(next_random() % 20 + 1);
    }
    long long total = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++)
        for (int c = 0; c < COUNT; c++) {
            long long a = count_upto(highs[c], ks[c]) - count_upto(lows[c] - 1, ks[c]);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    printf("%d ranges, %d rounds: %lld beautiful, checksum %lld\n", COUNT, ROUNDS, total, check);
    return 0;
}
