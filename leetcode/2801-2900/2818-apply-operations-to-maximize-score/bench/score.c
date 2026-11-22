// LeetCode #2818: Apply Operations to Maximize Score -- the bench's C
// mirror of the ★ arm: a sieve of prime scores, one monotonic stack, the
// indices sorted by value, largest first, by qsort, each power by
// squaring.

#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL

static long long power(long long base, long long exp) {
    long long result = 1, b = base % MOD, e = exp;
    while (e > 0) {
        if (e % 2 == 1) result = result * b % MOD;
        b = b * b % MOD;
        e /= 2;
    }
    return result;
}

static const long long *by_value;

static int larger_first(const void *a, const void *b) {
    long long x = by_value[*(const long long *)a], y = by_value[*(const long long *)b];
    return (x < y) - (x > y);
}

static long long maximum_score(const long long *nums, long long n, long long k) {
    long long top = 0;
    for (long long i = 0; i < n; i++) if (nums[i] > top) top = nums[i];
    long long *score = calloc(top + 1, sizeof *score);
    for (long long p = 2; p <= top; p++)
        if (score[p] == 0)
            for (long long q = p; q <= top; q += p) score[q]++;
    long long *s = malloc(n * sizeof *s), *left = malloc(n * sizeof *left);
    long long *right = malloc(n * sizeof *right), *stack = malloc(n * sizeof *stack);
    long long *order = malloc(n * sizeof *order);
    long long depth = 0;
    for (long long i = 0; i < n; i++) {
        s[i] = score[nums[i]];
        left[i] = -1;
        right[i] = n;
    }
    for (long long i = 0; i < n; i++) {
        while (depth > 0 && s[stack[depth - 1]] < s[i]) right[stack[--depth]] = i;
        if (depth > 0) left[i] = stack[depth - 1];
        stack[depth++] = i;
    }
    for (long long i = 0; i < n; i++) order[i] = i;
    by_value = nums;
    qsort(order, n, sizeof *order, larger_first);
    long long rest = k, total = 1;
    for (long long j = 0; j < n && rest > 0; j++) {
        long long i = order[j];
        long long take = (i - left[i]) * (right[i] - i);
        if (take > rest) take = rest;
        total = total * power(nums[i], take) % MOD;
        rest -= take;
    }
    free(score); free(s); free(left); free(right); free(stack); free(order);
    return total;
}

static long long seed = 2818;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long wide(void) {
    long long a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    enum { COUNT = 20, ROUNDS = 3, N = 100000 };
    static long long nums[COUNT][N];
    long long ks[COUNT];
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < N; i++) nums[c][i] = wide() % 100000 + 1;
        ks[c] = wide() % 1000000000 + 1;
    }
    long long total = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++)
        for (int c = 0; c < COUNT; c++) {
            long long a = maximum_score(nums[c], N, ks[c]);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    printf("%d arrays of %d, %d rounds: scores sum to %lld, checksum %lld\n", COUNT, N, ROUNDS, total, check);
    return 0;
}
