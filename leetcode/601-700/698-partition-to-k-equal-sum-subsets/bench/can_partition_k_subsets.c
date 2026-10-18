// LeetCode #698: Partition to K Equal Sum Subsets -- bench program, C mirror of the bottom-up arm.
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

static long long seed = 698;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static bool can_partition_k_subsets(const long long *nums, int n, long long k) {
    long long total = 0;
    for (int i = 0; i < n; i++) total += nums[i];
    if (total % k != 0) return false;
    long long target = total / k;
    long long size = 1LL << n;
    long long *fill = malloc(size * sizeof(long long));
    for (long long m = 0; m < size; m++) fill[m] = -1;
    fill[0] = 0;
    for (long long mask = 0; mask < size; mask++) {
        if (fill[mask] < 0) continue;
        for (int i = 0; i < n; i++) {
            long long next = mask | (1LL << i);
            if (next != mask && fill[next] < 0 && fill[mask] + nums[i] <= target)
                fill[next] = (fill[mask] + nums[i]) % target;
        }
    }
    bool ok = fill[size - 1] == 0;
    free(fill);
    return ok;
}

int main(void) {
    static long long problems[100][16];
    long long ks[100];
    for (int p = 0; p < 100; p++) {
        long long k = 1LL << (p % 5);
        long long g = 16 / k;
        long long target = 16 + next_random() % 9985;
        int len = 0;
        for (long long b = 0; b < k; b++) {
            long long left = target;
            for (long long q = 0; q < g - 1; q++) {
                long long part = 1 + next_random() % (target / g);
                problems[p][len++] = part;
                left -= part;
            }
            problems[p][len++] = left;
        }
        for (int i = 0; i < 16; i++) {
            int j = i + next_random() % (16 - i);
            long long t = problems[p][i];
            problems[p][i] = problems[p][j];
            problems[p][j] = t;
        }
        if (p % 2 == 1) {
            int i = next_random() % 16;
            int j = (i + 1 + next_random() % 15) % 16;
            long long most = problems[p][j] - 1;
            if (10000 - problems[p][i] < most) most = 10000 - problems[p][i];
            if (most >= 1) {
                long long d = 1 + next_random() % most;
                problems[p][i] += d;
                problems[p][j] -= d;
            }
        }
        ks[p] = k;
    }
    int rounds = 2;
    long long yes = 0, checksum = 0;
    for (int r = 0; r < rounds; r++)
        for (int p = 0; p < 100; p++) {
            bool ok = can_partition_k_subsets(problems[p], 16, ks[p]);
            if (ok) yes++;
            checksum = (checksum * 3 + (ok ? 1 : 0) + p) % 1000000007;
        }
    printf("%d rounds of 100 problems of 16 values: %lld answers yes, checksum %lld\n", rounds, yes, checksum);
    return 0;
}
