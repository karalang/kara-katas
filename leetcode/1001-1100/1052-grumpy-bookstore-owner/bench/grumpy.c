// LeetCode #1052: Grumpy Bookstore Owner -- C mirror of bench/grumpy.kara.
#include <stdio.h>
#include <stdlib.h>

static long long seed = 1052;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long max_satisfied(const long long *customers, const long long *grumpy, long long n, long long minutes) {
    long long base = 0, saved = 0, best = 0;
    for (long long i = 0; i < n; i++) {
        if (grumpy[i] == 0)
            base += customers[i];
        else
            saved += customers[i];
        if (i >= minutes && grumpy[i - minutes] == 1) saved -= customers[i - minutes];
        if (saved > best) best = saved;
    }
    return base + best;
}

int main(void) {
    enum { DAYS = 200, N = 20000, TECHNIQUES = 10 };
    long long *customers = malloc(sizeof(long long) * DAYS * N);
    long long *grumpy = malloc(sizeof(long long) * DAYS * N);
    for (int d = 0; d < DAYS; d++)
        for (int i = 0; i < N; i++) {
            customers[d * N + i] = next_random() % 1001;
            grumpy[d * N + i] = next_random() % 2;
        }
    long long total = 0, check = 0;
    for (int d = 0; d < DAYS; d++)
        for (int t = 0; t < TECHNIQUES; t++) {
            long long minutes = next_random() % N + 1;
            long long answer = max_satisfied(customers + d * N, grumpy + d * N, N, minutes);
            total += answer;
            check = (check * 131 + answer) % 1000000007;
        }
    printf("%d days of %d minutes, %d techniques each: total %lld, checksum %lld\n", DAYS, N, TECHNIQUES, total, check);
    free(customers);
    free(grumpy);
    return 0;
}
