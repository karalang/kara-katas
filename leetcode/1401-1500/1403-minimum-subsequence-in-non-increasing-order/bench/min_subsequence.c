// LeetCode #1403 bench, C: the same sort and greedy take, workload and
// checksum as min_subsequence.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define POOL 100000
#define WINDOW 500

static int by_value(const void *pa, const void *pb) {
    int32_t a = *(const int32_t *)pa, b = *(const int32_t *)pb;
    return (a > b) - (a < b);
}

// the picked numbers go to `picked`, largest first; returns how many
static int min_subsequence(const int32_t *nums, int n, int32_t *picked) {
    int32_t order[WINDOW];
    memcpy(order, nums, sizeof(int32_t) * n);
    qsort(order, n, sizeof(int32_t), by_value);
    int32_t rest = 0;
    for (int i = 0; i < n; i++) {
        rest += order[i];
    }
    int64_t taken = 0;
    int count = 0;
    for (int i = n - 1; i >= 0; i--) {
        picked[count++] = order[i];
        taken += order[i];
        rest -= order[i];
        if (taken > rest) {
            break;
        }
    }
    return count;
}

int main(void) {
    static int32_t pool[POOL];
    int64_t seed = 1403;
    for (int i = 0; i < POOL; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        pool[i] = (int32_t)(seed / 65536 % 100 + 1);
    }
    int64_t check = 0;
    int32_t window[WINDOW], picked[WINDOW];
    for (int64_t r = 0; r < 20000; r++) {
        int64_t at = (check + r * 7919) % 99501;
        memcpy(window, pool + at, sizeof(int32_t) * WINDOW);
        int count = min_subsequence(window, WINDOW, picked);
        check = (check * 131 + (int64_t)count * 101 + picked[count - 1]) % 1000000007;
    }
    printf("20000 windows of 500 numbers: checksum %lld\n", (long long)check);
    return 0;
}
