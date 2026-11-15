// LeetCode #2176: Count Equal and Divisible Pairs in an Array -- the
// benchmark's C mirror of pairs.kara, over a pointer and a length.

#include <stdio.h>
#include <stdlib.h>

static long long count_pairs(const long long *nums, long long n, long long k) {
    long long pairs = 0;
    for (long long i = 0; i < n; i++)
        for (long long j = i + 1; j < n; j++)
            if (nums[i] == nums[j] && i * j % k == 0) pairs++;
    return pairs;
}

static long long seed = 2176;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    long long *row = malloc(100000 * sizeof(long long));
    for (int i = 0; i < 100000; i++) row[i] = next_random() % 5 + 1;
    long long check = 0;
    for (int r = 0; r < 20000; r++) {
        long long start = next_random() % 99901;
        long long k = next_random() % 100 + 1;
        long long pairs = count_pairs(row + start, 100, k);
        check = (check * 31 + pairs) % 1000000007;
    }
    printf("20000 solves: checksum %lld\n", check);
    free(row);
    return 0;
}
