// LeetCode #1708: Largest Subarray Length K -- the C mirror of the bench
// (largest.kara): the largest first value among the starts that leave
// room for k, on 50 random arrays of 100000 distinct values, each
// answered 100 times.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// the answer copied into a new array, as the other languages return one
static int *largest_subarray(const int *nums, long n, long k) {
    long best = 0;
    for (long i = 1; i <= n - k; i++) {
        if (nums[i] > nums[best]) {
            best = i;
        }
    }
    int *answer = malloc(sizeof(int) * k);
    memcpy(answer, nums + best, sizeof(int) * k);
    return answer;
}

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int count = 50;
    const long long rounds = 100;
    const long n = 100000;
    long long seed = 1708;
    int *nums[50];
    long ks[50];
    for (int p = 0; p < count; p++) {
        nums[p] = malloc(sizeof(int) * n);
        for (long i = 0; i < n; i++) {
            nums[p][i] = (int)i;
        }
        for (long i = n - 1; i >= 1; i--) {
            long long a = next_random(&seed);
            long j = (long)((a * 32768 + next_random(&seed)) % (i + 1));
            int t = nums[p][i];
            nums[p][i] = nums[p][j];
            nums[p][j] = t;
        }
        for (long i = 0; i < n; i++) {
            nums[p][i] = nums[p][i] * 10000 + (int)(next_random(&seed) % 10000);
        }
        long long a = next_random(&seed);
        ks[p] = (long)((a * 32768 + next_random(&seed)) % n + 1);
    }
    long long chosen = 0;
    long long check = 0;
    for (long long r = 0; r < rounds; r++) {
        for (int p = 0; p < count; p++) {
            long k = ks[p];
            int *answer = largest_subarray(nums[p], n, k);
            chosen += k;
            check = (check * 31 + k + answer[0] + answer[k - 1] + r) % 1000000007;
            free(answer);
        }
    }
    printf("%d arrays of %ld values, %lld rounds: %lld chosen, checksum %lld\n", count, n, rounds, chosen, check);
    for (int p = 0; p < count; p++) {
        free(nums[p]);
    }
    return 0;
}
