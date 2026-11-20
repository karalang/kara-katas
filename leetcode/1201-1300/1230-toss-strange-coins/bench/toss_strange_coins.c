// LeetCode #1230 bench: the ★ arm in C, over the same 200 sets of 1000
// coins as the Kāra bench.
#include <stdio.h>
#include <stdlib.h>

static double probability_of_heads(const double *prob, long n, long target, double *ways) {
    for (long j = 0; j <= target; j++) ways[j] = 0.0;
    ways[0] = 1.0;
    for (long i = 0; i < n; i++) {
        double p = prob[i];
        for (long j = target; j >= 1; j--) ways[j] = ways[j] * (1.0 - p) + ways[j - 1] * p;
        ways[0] = ways[0] * (1.0 - p);
    }
    return ways[target];
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

int main(void) {
    long seed = 1230;
    double *sets = malloc(sizeof(double) * 200 * 1000);
    long targets[200];
    for (int s = 0; s < 200; s++) {
        for (int i = 0; i < 1000; i++) sets[s * 1000 + i] = (double)(next_random(&seed) % 1001) / 1000.0;
        targets[s] = next_random(&seed) % 1001;
    }
    double *ways = malloc(sizeof(double) * 1001);
    double total = 0.0;
    for (int s = 0; s < 200; s++) total += probability_of_heads(sets + s * 1000, 1000, targets[s], ways);
    printf("200 sets of 1000 coins: total %.6f\n", total);
    free(ways);
    free(sets);
    return 0;
}
