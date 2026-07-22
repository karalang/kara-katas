/* LeetCode 191 popcount benchmark kernel (C mirror, clang -O3). */
#include <stdio.h>
#include <stdlib.h>

static long hamming_weight(long n) {
    long count = 0, x = n;
    while (x != 0) { x = x & (x - 1); count++; }
    return count;
}

int main(void) {
    const long n = 2000000, k = 10;
    long *nums = malloc((size_t)n * sizeof(long));
    long state = 12345;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) % 2147483648L;
        nums[i] = state;
    }
    long sink = 0;
    for (long round = 0; round < k; round++)
        for (long j = 0; j < n; j++)
            sink += hamming_weight(nums[j] ^ round);
    printf("%ld\n", sink);
    free(nums);
    return 0;
}
