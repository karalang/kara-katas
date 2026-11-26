// LeetCode #1497: Check If Array Pairs Are Divisible by k -- the bench in
// C, mirroring can_arrange.kara: each value's remainder by k counted.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100000

static bool can_arrange(const int32_t *arr, int64_t n, int32_t k) {
    int64_t *count = calloc(k, sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) count[(arr[i] % k + k) % k]++;
    bool ok = count[0] % 2 == 0;
    for (int32_t r = 1; ok && r < k; r++)
        if (count[r] != count[k - r]) ok = false;
    free(count);
    return ok;
}

static int32_t arr[N];

int main(void) {
    int64_t seed = 1497;
    for (int64_t i = 0; i < N; i += 2) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t x = seed / 65536 * 30011 % 2000000001 - 1000000000;
        arr[i] = (int32_t)x;
        arr[i + 1] = (int32_t)(1000 * (seed % 7) - x);
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 1000; call++) {
        int64_t k = call % 2 == 0 ? 1000 : 1 + (check + call) % 100000;
        int64_t at = (check * 7 + call) % N;
        arr[at] = (int32_t)(arr[at] + (call % 4 < 2 ? 1000 : -1000));
        bool yes = can_arrange(arr, N, (int32_t)k);
        check = (check * 31 + k + (yes ? 2 : 1)) % 1000000007;
    }
    printf("1000 calls over 100000 values: checksum %lld\n", (long long)check);
    return 0;
}
