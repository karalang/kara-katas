// LeetCode #2031: Count Subarrays With More Ones Than Zeros -- the ★ arm in
// C, the same algorithm and workload as subarrays.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007LL

static int64_t subarrays_more_ones(const int64_t *nums, int64_t n) {
    int64_t *seen = calloc((size_t)(2 * n + 1), sizeof(int64_t));
    int64_t prefix = n;
    seen[prefix] = 1;
    int64_t below = 0, total = 0;
    for (int64_t i = 0; i < n; i++) {
        if (nums[i] == 1) {
            below += seen[prefix];
            prefix++;
        } else {
            prefix--;
            below -= seen[prefix];
        }
        total = (total + below) % MOD;
        seen[prefix]++;
    }
    free(seen);
    return total;
}

static int64_t seed = 2031;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t arrays[20][100000];
    for (int64_t a = 0; a < 20; a++)
        for (int i = 0; i < 100000; i++)
            arrays[a][i] = next_random() % 10 < a % 9 + 1 ? 1 : 0;
    int64_t calls = 0, sum = 0, check = 0;
    for (int64_t round = 0; round < 100; round++) {
        for (int64_t a = 0; a < 20; a++) {
            int64_t at = (round * 997 + a * 31) % 100000;
            arrays[a][at] = 1 - arrays[a][at];
            int64_t answer = subarrays_more_ones(arrays[a], 100000);
            calls++;
            sum = (sum + answer) % MOD;
            check = (check * 31 + answer) % MOD;
        }
    }
    printf("%lld calls: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    return 0;
}
