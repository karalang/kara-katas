// LeetCode #2425: Bitwise XOR of All Pairings -- the bench, the ★ arm: the
// XOR of `nums1` when `nums2` has odd length, XORed with that of `nums2`
// when `nums1` has odd length.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t xor_all_nums(const int64_t *nums1, int64_t n, const int64_t *nums2, int64_t m) {
    int64_t answer = 0;
    if (m % 2 == 1)
        for (int64_t i = 0; i < n; i++) answer ^= nums1[i];
    if (n % 2 == 1)
        for (int64_t j = 0; j < m; j++) answer ^= nums2[j];
    return answer;
}

static int64_t seed = 2425;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t *lists[2][10];
    int64_t lens[2][10];
    for (int64_t i = 0; i < 10; i++) {
        for (int which = 0; which < 2; which++) {
            int64_t n = which == 0 ? 100000 - i : 100000 - i / 2 - 1;
            int64_t *nums = malloc((size_t)n * sizeof(int64_t));
            for (int64_t k = 0; k < n; k++) {
                int64_t a = next_random();
                nums[k] = (a * 32768 + next_random()) % 1000000001;
            }
            lists[which][i] = nums;
            lens[which][i] = n;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 500; p++) {
        for (int i = 0; i < 10; i++) {
            int64_t at = (p * 7919) % lens[0][i];
            lists[0][i][at] ^= p % 1024;
            check = (check * 31 + xor_all_nums(lists[0][i], lens[0][i], lists[1][i], lens[1][i]) + p) % 1000000007;
        }
    }
    printf("500 passes over 10 pairs of 10^5 values: checksum %lld\n", (long long)check);
    for (int i = 0; i < 10; i++) {
        free(lists[0][i]);
        free(lists[1][i]);
    }
    return 0;
}
