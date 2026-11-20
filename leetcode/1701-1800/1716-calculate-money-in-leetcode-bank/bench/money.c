// LeetCode #1716: Calculate Money in Leetcode Bank -- the C mirror of the
// bench (money.kara): whole weeks and the days left in closed form, on
// 500000 random n, each answered 20 times.
#include <stdio.h>
#include <stdlib.h>

static int total_money(int n) {
    int weeks = n / 7;
    int days = n % 7;
    return 28 * weeks + 7 * weeks * (weeks - 1) / 2 + days * (weeks + 1) + days * (days - 1) / 2;
}

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int count = 500000;
    const long long rounds = 20;
    long long seed = 1716;
    int *ns = malloc(sizeof(int) * count);
    for (int i = 0; i < count; i++) {
        ns[i] = (int)(next_random(&seed) % 1000 + 1);
    }
    long long sum = 0;
    long long check = 0;
    for (long long r = 0; r < rounds; r++) {
        for (int i = 0; i < count; i++) {
            long long answer = total_money(ns[i]);
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d values of n, %lld rounds: answers sum to %lld, checksum %lld\n", count, rounds, sum, check);
    free(ns);
    return 0;
}
