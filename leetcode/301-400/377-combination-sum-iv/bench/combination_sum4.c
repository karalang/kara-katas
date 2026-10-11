// Benchmark for #377: mirror of combination_sum4.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define CAP 2147483648LL

static int64_t combination_sum4(const int64_t *nums, int n, int64_t target) {
    int64_t *ways = calloc((size_t)target + 1, sizeof *ways);
    ways[0] = 1;
    for (int64_t t = 1; t <= target; t++) {
        for (int i = 0; i < n; i++) {
            int64_t x = nums[i];
            if (x <= t) {
                int64_t s = ways[t] + ways[t - x];
                ways[t] = s < CAP ? s : CAP;
            }
        }
    }
    int64_t r = ways[target];
    free(ways);
    return r;
}

int main(void) {
    int64_t seed = 377, checksum = 0;
    int64_t nums[200];
    for (int c = 0; c < 2000; c++) {
        int n = 0;
        while (n < 200) {
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            int64_t v = 125 + (seed / 65536) % 875;
            int seen = 0;
            for (int i = 0; i < n; i++) {
                if (nums[i] == v) {
                    seen = 1;
                    break;
                }
            }
            if (!seen) nums[n++] = v;
        }
        checksum = (checksum * 1009 + combination_sum4(nums, n, 1000)) % 1000000007;
    }
    printf("checksum %lld\n", (long long)checksum);
    return 0;
}
