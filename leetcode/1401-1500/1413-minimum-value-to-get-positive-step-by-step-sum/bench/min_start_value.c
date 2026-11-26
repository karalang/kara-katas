#include <stdint.h>
#include <stdio.h>

static int32_t pool[100000];

static int32_t min_start_value(const int32_t *nums, int64_t n) {
    int32_t sum = 0, lowest = 0;
    for (int64_t i = 0; i < n; i++) {
        sum += nums[i];
        if (sum < lowest) lowest = sum;
    }
    return 1 - lowest;
}

int main(void) {
    int64_t seed = 1413;
    for (int i = 0; i < 100000; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        pool[i] = (int32_t)(seed / 65536 % 201 - 100);
    }
    int64_t check = 0;
    for (int i = 0; i < 3000000; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t start = seed / 65536 % 99901;
        check = (check * 131 + min_start_value(pool + start, 100)) % 1000000007;
    }
    printf("3 * 10^6 windows of 100 numbers: checksum %lld\n", (long long)check);
    return 0;
}
