// LeetCode #1130: Minimum Cost Tree From Leaf Values -- the bench in C, the
// same algorithm and workload as mct_from_leaf_values.kara: each array of
// leaves allocated by itself, a growable stack allocated per call, the
// same 4096 arrays and 400 rounds.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t mct_from_leaf_values(const int64_t *arr, int64_t n) {
    int64_t cost = 0;
    int64_t len = 0, cap = 4;
    int64_t *stack = malloc(cap * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        int64_t a = arr[i];
        while (len > 0 && stack[len - 1] <= a) {
            int64_t mid = stack[--len];
            int64_t partner = len > 0 ? (stack[len - 1] < a ? stack[len - 1] : a) : a;
            cost += mid * partner;
        }
        if (len == cap) {
            cap *= 2;
            stack = realloc(stack, cap * sizeof(int64_t));
        }
        stack[len++] = a;
    }
    while (len > 1) {
        int64_t top = stack[--len];
        cost += top * stack[len - 1];
    }
    free(stack);
    return cost;
}

static int64_t seed = 1130;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t *arrays[4096];
    for (int j = 0; j < 4096; j++) {
        arrays[j] = malloc(40 * sizeof(int64_t));
        for (int i = 0; i < 40; i++) arrays[j][i] = next_random() % 15 + 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 400; round++) {
        for (int64_t j = 0; j < 4096; j++) {
            int64_t at = (round * 7919 + j * 104729) % 40;
            arrays[j][at] = arrays[j][at] % 15 + 1;
            int64_t c = mct_from_leaf_values(arrays[j], 40);
            total += c;
            check = (check * 31 + c) % 1000000007;
        }
    }
    printf("400 rounds over 4096 arrays of 40 leaves: costs total %lld, checksum %lld\n",
           (long long)total, (long long)check);
    for (int j = 0; j < 4096; j++) free(arrays[j]);
    return 0;
}
