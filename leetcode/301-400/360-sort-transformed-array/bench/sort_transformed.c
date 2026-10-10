// Benchmark for #360 -- mirror of sort_transformed.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t f(int64_t x, int64_t a, int64_t b, int64_t c) {
    return a * x * x + b * x + c;
}

static void sort_transformed_array(const int64_t *nums, int64_t n, int64_t a, int64_t b, int64_t c, int64_t *out) {
    int64_t lo = 0, hi = n - 1;
    if (a >= 0) {
        int64_t k = n - 1;
        while (lo <= hi) {
            int64_t left = f(nums[lo], a, b, c), right = f(nums[hi], a, b, c);
            if (left >= right) { out[k] = left; lo++; } else { out[k] = right; hi--; }
            k--;
        }
    } else {
        int64_t k = 0;
        while (lo <= hi) {
            int64_t left = f(nums[lo], a, b, c), right = f(nums[hi], a, b, c);
            if (left <= right) { out[k] = left; lo++; } else { out[k] = right; hi--; }
            k++;
        }
    }
}

int main(void) {
    int64_t seed = 360, checksum = 0;
    int64_t *nums = malloc(sizeof(int64_t) * 50000);
    for (int round = 0; round < 200; round++) {
        int64_t x = -1000000;
        for (int i = 0; i < 50000; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            x += (seed / 65536) % 81;
            nums[i] = x;
        }
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t a = (seed / 65536) % 21 - 10;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t b = (seed / 65536) % 21 - 10;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t c = (seed / 65536) % 21 - 10;
        // A fresh output per array, as the Kara version allocates one.
        int64_t *out = malloc(sizeof(int64_t) * 50000);
        sort_transformed_array(nums, 50000, a, b, c, out);
        for (int i = 0; i < 50000; i++)
            checksum = (checksum * 31 + out[i] % 1000000007 + 1000000007) % 1000000007;
        free(out);
    }
    printf("checksum %lld\n", (long long)checksum);
    free(nums);
    return 0;
}
