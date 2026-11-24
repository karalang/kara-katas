// LeetCode #2447: Number of Subarrays With GCD Equal to K -- the bench,
// the ★ arm: from each start the running GCD, the walk stopped once it
// is no multiple of `k`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t gcd(int64_t a, int64_t b) {
    int64_t x = a, y = b;
    while (y != 0) {
        int64_t r = x % y;
        x = y;
        y = r;
    }
    return x;
}

static int64_t subarray_gcd(const int64_t *nums, int64_t n, int64_t k) {
    int64_t count = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t g = 0;
        for (int64_t j = i; j < n; j++) {
            g = gcd(g, nums[j]);
            if (g % k != 0) break;
            if (g == k) count++;
        }
    }
    return count;
}

static int64_t seed = 2447;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t draw(void) {
    int64_t v = 6 * (1 + next_random() % 1000);
    return next_random() % 40 == 0 ? v + 1 : v;
}

int main(void) {
    int64_t *arrays[20];
    for (int c = 0; c < 20; c++) {
        arrays[c] = malloc(1000 * sizeof(int64_t));
        for (int i = 0; i < 1000; i++) arrays[c][i] = draw();
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 90; p++)
        for (int64_t c = 0; c < 20; c++) {
            arrays[c][(37 * p + c) % 1000] = draw();
            check = (check * 31 + subarray_gcd(arrays[c], 1000, 6) + p) % 1000000007;
        }
    printf("90 passes over 20 arrays of 1000 values: checksum %lld\n", (long long)check);
    for (int c = 0; c < 20; c++) free(arrays[c]);
    return 0;
}
