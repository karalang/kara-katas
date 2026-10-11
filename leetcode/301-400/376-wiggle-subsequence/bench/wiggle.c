// Benchmark for #376 -- mirror of wiggle.kara.

#include <stdint.h>
#include <stdio.h>

static int64_t wiggle_max_length(const int64_t *nums, int64_t n) {
    if (n == 0) return 0;
    int64_t up = 1, down = 1;
    for (int64_t i = 1; i < n; i++) {
        if (nums[i] > nums[i - 1]) up = down + 1;
        else if (nums[i] < nums[i - 1]) down = up + 1;
    }
    return up > down ? up : down;
}

int main(void) {
    int64_t seed = 376, checksum = 0;
    static int64_t nums[1000];
    for (int c = 0; c < 20000; c++) {
        int64_t top = c % 3 == 0 ? 6 : 1001;
        for (int i = 0; i < 1000; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            nums[i] = (seed / 65536) % top;
        }
        checksum = (checksum * 1009 + wiggle_max_length(nums, 1000)) % 1000000007;
    }
    printf("checksum %lld\n", (long long)checksum);
    return 0;
}
