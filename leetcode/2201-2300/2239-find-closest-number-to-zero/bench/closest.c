// LeetCode #2239: Find Closest Number to Zero -- the benchmark's C
// mirror of closest.kara: one scan, a number kept when nearer to zero,
// or as near and larger.
#include <stdint.h>
#include <stdio.h>

static int64_t magnitude(int64_t x) { return x < 0 ? -x : x; }

static int64_t find_closest_number(const int64_t *nums, int64_t n) {
    int64_t closest = nums[0];
    for (int64_t i = 0; i < n; i++) {
        int64_t x = nums[i];
        if (magnitude(x) < magnitude(closest) || (magnitude(x) == magnitude(closest) && x > closest)) closest = x;
    }
    return closest;
}

static int64_t seed = 2239;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    int64_t nums[1000];
    for (int i = 0; i < 1000; i++) nums[i] = wide_random() % 200001 - 100000;
    int64_t check = 0;
    for (int pass = 0; pass < 100000; pass++) {
        // punch: one number drawn again before each pass
        int64_t at = next_random() % 1000;
        nums[at] = wide_random() % 200001 - 100000;
        check = (check * 31 + find_closest_number(nums, 1000) + 100000) % 1000000007;
    }
    printf("100000 passes over 1000 numbers: checksum %lld\n", (long long)check);
    return 0;
}
