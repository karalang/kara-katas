// LeetCode #2341: Maximum Number of Pairs in Array -- the bench, the ★ arm
// in C: each value counted in a table of 101, the pairs every count's half
// and the leftovers its parity.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static void number_of_pairs(const int64_t *nums, int64_t n, int64_t *answer) {
    int64_t *counts = calloc(101, sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) counts[nums[i]] += 1;
    int64_t pairs = 0, left = 0;
    for (int v = 0; v < 101; v++) {
        pairs += counts[v] / 2;
        left += counts[v] % 2;
    }
    free(counts);
    answer[0] = pairs;
    answer[1] = left;
}

static int64_t scrambled(int64_t index) { return index * 2654435761LL % 2147483647LL; }

int main(void) {
    int64_t *arrays[10];
    for (int64_t a = 0; a < 10; a++) {
        arrays[a] = malloc(100000 * sizeof(int64_t));
        for (int64_t i = 0; i < 100000; i++) arrays[a][i] = scrambled(a * 100000 + i) % 101;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 50; p++) {
        for (int a = 0; a < 10; a++) {
            int64_t answer[2];
            number_of_pairs(arrays[a], 100000, answer);
            check = (check * 31 + answer[0] * 101 + answer[1] + p) % 1000000007;
        }
    }
    printf("50 passes over 10 arrays of 10^5 values: checksum %lld\n", (long long)check);
    for (int a = 0; a < 10; a++) free(arrays[a]);
    return 0;
}
