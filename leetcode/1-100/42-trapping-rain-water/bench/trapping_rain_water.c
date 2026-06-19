// LeetCode #42 bench mirror — C, the converging two-pointer solver (★).
//
// Mirrors bench/trapping_rain_water.kara: advance the shorter outer wall, settling each
// column with its running max. The buffer is allocated once and overwritten in place each
// iteration with a k-dependent jagged terrain. Same workload (TOTAL refills) and the same
// answer-fold checksum as every other mirror.

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static int64_t trap(const int64_t *height, int64_t n) {
    int64_t left = 0, right = n - 1;
    int64_t left_max = 0, right_max = 0;
    int64_t water = 0;
    while (left < right) {
        if (height[left] < height[right]) {
            if (height[left] >= left_max) {
                left_max = height[left];
            } else {
                water += left_max - height[left];
            }
            left++;
        } else {
            if (height[right] >= right_max) {
                right_max = height[right];
            } else {
                water += right_max - height[right];
            }
            right--;
        }
    }
    return water;
}

int main(void) {
    const int64_t total = 200000;
    const int64_t n = 1000;
    const int64_t modulus = 1000000007;

    int64_t *height = (int64_t *)malloc((size_t)n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        height[i] = (i * 37) % 100;
    }

    int64_t acc = 0;
    for (int64_t k = 0; k < total; k++) {
        height[k % n] = (k * 19) % 100;
        int64_t ans = trap(height, n);
        acc = (acc * 131 + ans) % modulus;
    }

    free(height);
    printf("%lld\n", (long long)acc);
    return 0;
}
