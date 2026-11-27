// LeetCode #1806: Minimum Number of Operations to Reinitialize a
// Permutation -- the bench in C: the ★ arm over 3000 calls, each n an even
// number to 1000 drawn from the checksum so far.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int32_t reinitialize_permutation(int32_t n) {
    int64_t size = n;
    int64_t *start = malloc(sizeof(int64_t) * size);
    int64_t *perm = malloc(sizeof(int64_t) * size);
    for (int64_t i = 0; i < size; i++) start[i] = perm[i] = i;
    int32_t ops = 0;
    for (;;) {
        int64_t *arr = calloc(size, sizeof(int64_t));
        for (int64_t i = 0; i < size; i++)
            arr[i] = i % 2 == 0 ? perm[i / 2] : perm[size / 2 + (i - 1) / 2];
        free(perm);
        perm = arr;
        ops++;
        if (memcmp(perm, start, sizeof(int64_t) * size) == 0) break;
    }
    free(perm);
    free(start);
    return ops;
}

int main(void) {
    int64_t check = 0;
    for (int64_t call = 0; call < 3000; call++) {
        int64_t n = 2 * (1 + (check + call) % 500);
        check = (check * 31 + reinitialize_permutation((int32_t)n)) % 1000000007;
    }
    printf("3000 calls of even n to 1000: checksum %lld\n", (long long)check);
    return 0;
}
