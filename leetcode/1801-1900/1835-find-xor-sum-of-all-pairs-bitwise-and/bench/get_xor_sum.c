// LeetCode #1835: Find XOR Sum of All Pairs Bitwise AND -- the bench in C: the ★ arm over
// 3000 calls on pairs of 20 lists of 10^5 numbers from 0 to 10^9, built
// once, each call's two lists drawn from the checksum so far. The arm
// borrows both lists, so no call copies one.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t get_xor_sum(const int64_t *arr1, int64_t n, const int64_t *arr2, int64_t m) {
    int64_t left = 0;
    for (int64_t k = 0; k < n; k++) left ^= arr1[k];
    int64_t right = 0;
    for (int64_t k = 0; k < m; k++) right ^= arr2[k];
    return left & right;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1835;
    int64_t *lists[20];
    for (int l = 0; l < 20; l++) {
        lists[l] = malloc(100000 * sizeof(int64_t));
        for (int64_t k = 0; k < 100000; k++) {
            int64_t hi = next_random(&seed);
            lists[l][k] = (hi * 32768 + next_random(&seed)) % 1000000001;
        }
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 3000; call++) {
        int64_t i = (check + call) % 20;
        int64_t j = (check / 20 + call * 7) % 20;
        check = (check * 31 + get_xor_sum(lists[i], 100000, lists[j], 100000)) % 1000000007;
    }
    printf("3000 calls: checksum %lld\n", (long long)check);
    return 0;
}
