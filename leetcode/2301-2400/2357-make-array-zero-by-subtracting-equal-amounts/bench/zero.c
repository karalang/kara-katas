// LeetCode #2357: Make Array Zero by Subtracting Equal Amounts -- the
// bench, the ★ arm in C: the distinct positive values gathered in a set.
// C has no set, so it is a table of 256 slots by open addressing, cleared
// for each call.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 256

static int64_t minimum_operations(const int64_t *nums, int n) {
    int64_t table[SLOTS];
    memset(table, 0, sizeof table);
    int64_t count = 0;
    for (int i = 0; i < n; i++) {
        int64_t x = nums[i];
        if (x <= 0) {
            continue;
        }
        size_t s = ((uint64_t)x * 0x9E3779B97F4A7C15ULL) >> 56;
        while (table[s] != 0 && table[s] != x) {
            s = (s + 1) & (SLOTS - 1);
        }
        if (table[s] == 0) {
            table[s] = x;
            count++;
        }
    }
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // 2 * 10^4 arrays of 100 values from 0 to 1 up to 0 to 100
    int64_t seed = 2357;
    int64_t *arrays = malloc(20000 * 100 * sizeof(int64_t));
    for (int a = 0; a < 20000; a++) {
        int64_t top = 2 + next_random(&seed) % 100;
        for (int i = 0; i < 100; i++) {
            arrays[a * 100 + i] = next_random(&seed) % top;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 50; p++) {
        for (int a = 0; a < 20000; a++) {
            check = (check * 31 + minimum_operations(arrays + a * 100, 100) + p) % 1000000007;
        }
    }
    printf("50 passes over 2 * 10^4 arrays of 100 values: checksum %lld\n", (long long)check);
    free(arrays);
    return 0;
}
