// benchmark's C mirror of minimal.kara (LeetCode #2195, the ★ arm): the
// gaps walked, each a series.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long long run_sum(long long from, long long to) {
    return (from + to) * (to - from + 1) / 2;
}

static int cmp(const void *a, const void *b) {
    long long x = *(const long long *)a, y = *(const long long *)b;
    return (x > y) - (x < y);
}

static long long minimal_k_sum(const long long *nums, int n, long long k) {
    long long *sorted = malloc(sizeof(long long) * n);
    memcpy(sorted, nums, sizeof(long long) * n);
    qsort(sorted, n, sizeof(long long), cmp);
    long long wanted = k, sum = 0, last = 0;
    for (int i = 0; i < n; i++) {
        long long x = sorted[i];
        if (x > last + 1 && wanted > 0) {
            long long take = x - last - 1 < wanted ? x - last - 1 : wanted;
            sum += run_sum(last + 1, last + take);
            wanted -= take;
        }
        if (x > last) last = x;
    }
    if (wanted > 0) sum += run_sum(last + 1, last + wanted);
    free(sorted);
    return sum;
}

static long long seed = 2195;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int n = 100000;
    long long *nums = malloc(sizeof(long long) * n);
    for (int i = 0; i < n; i++) {
        long long a = next_random();
        long long b = next_random();
        nums[i] = (a * 32768 + b) % 1000000000 + 1;
    }
    long long check = 0;
    for (int i = 0; i < 300; i++) {
        long long k = 100000000 - (long long)i * 1000;
        check = (check * 31 + minimal_k_sum(nums, n, k) % 1000000007) % 1000000007;
    }
    printf("300 solves over %d numbers: checksum %lld\n", n, check);
    free(nums);
    return 0;
}
