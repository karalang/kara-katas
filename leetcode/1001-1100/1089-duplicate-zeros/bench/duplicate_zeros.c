// Benchmark: LeetCode #1089 Duplicate Zeros -- mirrors duplicate_zeros.kara:
// count the zeros, then walk back from the end writing each digit at its
// place shifted by the zeros up to it, over 200 random arrays of 10^4
// digits built once, each copied into its own allocation and duplicated in
// each of 100 rounds.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ARRAYS 200
#define LEN 10000

static void duplicate_zeros(int64_t *arr, int64_t n) {
    int64_t zeros = 0;
    for (int64_t i = 0; i < n; i++) {
        if (arr[i] == 0) {
            zeros++;
        }
    }
    for (int64_t i = n - 1; i >= 0; i--) {
        if (i + zeros < n) {
            arr[i + zeros] = arr[i];
        }
        if (arr[i] == 0) {
            zeros--;
            if (i + zeros < n) {
                arr[i + zeros] = 0;
            }
        }
    }
}

static int64_t seed = 1089;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t *arrays[ARRAYS];
    for (int k = 0; k < ARRAYS; k++) {
        arrays[k] = malloc(LEN * sizeof(int64_t));
        for (int i = 0; i < LEN; i++) {
            int64_t r = next_random() % 15;
            arrays[k][i] = r < 5 ? 0 : r - 5;
        }
    }
    int64_t zeros = 0, check = 0;
    for (int64_t round = 0; round < 100; round++) {
        for (int64_t k = 0; k < ARRAYS; k++) {
            int64_t *work = malloc(LEN * sizeof(int64_t));
            memcpy(work, arrays[k], LEN * sizeof(int64_t));
            duplicate_zeros(work, LEN);
            int64_t at = (round * 7919 + k * 31) % LEN;
            if (work[at] == 0) {
                zeros++;
            }
            check = (check * 31 + work[at] * 10 + work[LEN - 1]) % 1000000007;
            free(work);
        }
    }
    printf("100 rounds over 200 arrays of 10^4 digits: %lld zeros sampled, checksum %lld\n",
           (long long)zeros, (long long)check);
    for (int k = 0; k < ARRAYS; k++) {
        free(arrays[k]);
    }
    return 0;
}
