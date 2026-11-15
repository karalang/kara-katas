// benchmark's C mirror of replace.kara (LeetCode #2197, the ★ arm): a
// stack merged at its top.
#include <stdio.h>
#include <stdlib.h>

static long long gcd(long long a, long long b) {
    while (b != 0) {
        long long r = a % b;
        a = b;
        b = r;
    }
    return a;
}

static int replace_non_coprimes(const long long *nums, int n, long long *stack) {
    int top = 0;
    for (int i = 0; i < n; i++) {
        long long cur = nums[i];
        while (top > 0) {
            long long g = gcd(stack[top - 1], cur);
            if (g == 1) break;
            cur = stack[top - 1] / g * cur;
            top--;
        }
        stack[top++] = cur;
    }
    return top;
}

static long long seed = 2197;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long wide_random(void) {
    long long a = next_random();
    return a * 32768 + next_random();
}

static int divisors(long long m, long long *out) {
    int k = 0;
    for (long long d = 1; d <= 100000; d++)
        if (m % d == 0) out[k++] = d;
    return k;
}

#define N 100000

int main(void) {
    static long long pools[3][512];
    int sizes[3];
    sizes[0] = divisors(10810800, pools[0]);
    sizes[1] = divisors(1674432, pools[1]);
    long long primes[7] = {1, 99991, 99989, 99971, 99961, 99929, 99923};
    for (int i = 0; i < 7; i++) pools[2][i] = primes[i];
    sizes[2] = 7;
    static long long arrays[12][N];
    for (int a = 0; a < 12; a++)
        for (int i = 0; i < N; i++) arrays[a][i] = pools[a % 3][wide_random() % sizes[a % 3]];
    long long *stack = malloc(sizeof(long long) * N);
    long long check = 0;
    for (int pass = 0; pass < 100; pass++) {
        for (int a = 0; a < 12; a++) {
            int len = replace_non_coprimes(arrays[a], N, stack);
            check = (check * 31 + len) % 1000000007;
            check = (check * 31 + stack[len / 2]) % 1000000007;
        }
    }
    printf("100 passes over 12 arrays: checksum %lld\n", check);
    free(stack);
    return 0;
}
