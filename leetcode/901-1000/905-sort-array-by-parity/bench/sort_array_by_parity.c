// LeetCode #905: Sort Array By Parity -- bench program, C.
//
// The two pointers from both ends, over 1,000,000 numbers below 5001 built
// once. Each round sorts a copy by parity, folds the evens in front and
// one number of the answer into a checksum and changes one number.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void sort_array_by_parity(int64_t *out, int64_t n) {
    int64_t i = 0, j = n - 1;
    while (i < j) {
        if (out[i] % 2 == 0) {
            i += 1;
        } else if (out[j] % 2 == 1) {
            j -= 1;
        } else {
            int64_t t = out[i];
            out[i] = out[j];
            out[j] = t;
            i += 1;
            j -= 1;
        }
    }
}

static int64_t seed = 905;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t n = 1000000;
    int64_t rounds = 100;
    int64_t *nums = malloc(sizeof(int64_t) * n);
    for (int64_t k = 0; k < n; k++) nums[k] = next_random() % 5001;
    int64_t check = 0, total = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t *out = malloc(sizeof(int64_t) * n);
        memcpy(out, nums, sizeof(int64_t) * n);
        sort_array_by_parity(out, n);
        int64_t lead = 0;
        while (out[lead] % 2 == 0) lead += 1;
        total += lead;
        check = (check * 31 + lead) % 1000000007;
        check = (check * 31 + out[round * 7919 % n]) % 1000000007;
        free(out);
        nums[round * 7919 % n] = next_random() % 5001;
    }
    printf("%lld rounds over %lld numbers: %lld evens in front, checksum %lld\n", (long long)rounds,
           (long long)n, (long long)total, (long long)check);
    free(nums);
    return 0;
}
