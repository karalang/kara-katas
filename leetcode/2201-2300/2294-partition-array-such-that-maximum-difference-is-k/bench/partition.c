// LeetCode #2294: Partition Array Such That Maximum Difference Is K --
// the bench, the ★ arm in C. Sort a copy with qsort, then open a group at
// each number more than k above the one that opened the last.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum { ARRAYS = 20, N = 100000 };

static int cmp(const void *a, const void *b) {
    int64_t x = *(const int64_t *)a, y = *(const int64_t *)b;
    return (x > y) - (x < y);
}

static int64_t partition_array(const int64_t *nums, int n, int64_t k, int64_t *sorted) {
    memcpy(sorted, nums, sizeof(int64_t) * n);
    qsort(sorted, n, sizeof(int64_t), cmp);
    int64_t groups = 0, low = -1;
    for (int i = 0; i < n; i++) {
        if (groups == 0 || sorted[i] - low > k) {
            groups++;
            low = sorted[i];
        }
    }
    return groups;
}

static int64_t seed = 2294;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t arrays[ARRAYS][N];
    static int64_t sorted[N];
    for (int a = 0; a < ARRAYS; a++)
        for (int i = 0; i < N; i++) {
            int64_t hi = next_random();
            arrays[a][i] = (hi * 32768 + next_random()) % 100001;
        }
    int64_t check = 0;
    for (int64_t p = 0; p < 5; p++)
        for (int a = 0; a < ARRAYS; a++) check = (check * 31 + partition_array(arrays[a], N, 7 * a + p, sorted)) % 1000000007;
    printf("5 passes over 20 arrays of 10^5: checksum %lld\n", (long long)check);
    return 0;
}
