// LeetCode #1390 bench, C mirror of the ★ arm.
#include <stdint.h>
#include <stdio.h>

static int32_t sum_four_divisors(const int32_t *nums, int n) {
    int32_t total = 0;
    for (int k = 0; k < n; k++) {
        int32_t v = nums[k];
        int count = 0;
        int32_t sum = 0;
        int32_t d = 1;
        while (d * d <= v && count <= 4) {
            if (v % d == 0) {
                count += 1;
                sum += d;
                if (d * d != v) {
                    count += 1;
                    sum += v / d;
                }
            }
            d += 1;
        }
        if (count == 4) total += sum;
    }
    return total;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    enum { N = 10000 };
    static int32_t nums[N];
    int64_t seed = 1390;
    for (int k = 0; k < N; k++) {
        int64_t a = next_random(&seed);
        int64_t b = next_random(&seed);
        nums[k] = (int32_t)(1 + (a * 32768 + b) % 100000);
    }
    int64_t check = 0;
    for (int r = 0; r < 300; r++) {
        seed = (seed + check) % 2147483648LL;
        int64_t i = next_random(&seed) % N;
        int64_t a = next_random(&seed);
        int64_t b = next_random(&seed);
        nums[i] = (int32_t)(1 + (a * 32768 + b) % 100000);
        check = (check * 131 + sum_four_divisors(nums, N)) % 1000000007;
    }
    printf("300 rounds over 10^4 values up to 10^5: checksum %lld\n", (long long)check);
    return 0;
}
