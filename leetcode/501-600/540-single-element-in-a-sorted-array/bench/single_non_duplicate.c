// Benchmark for #540: C mirror of the ★ arm (binary search over the
// pairs); see single_non_duplicate.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t single_non_duplicate(const int64_t *nums, int64_t n) {
    int64_t low = 0, high = n - 1;
    while (low < high) {
        int64_t mid = (low + high) / 2;
        if (mid % 2 == 1) mid -= 1;
        if (nums[mid] == nums[mid + 1]) {
            low = mid + 2;
        } else {
            high = mid;
        }
    }
    return nums[low];
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    // 100 arrays of 0 to 49,999 pairs and the single element at a
    // random place, values rising by 1 or 2, built once. Then the answer
    // for each array is found 200,000 times.
    int64_t arrays = 100;
    int64_t seed = 540;
    int64_t **all = malloc(arrays * sizeof(int64_t *));
    int64_t *lens = malloc(arrays * sizeof(int64_t));
    int64_t elements = 0;
    for (int64_t t = 0; t < arrays; t++) {
        int64_t high = next_random(&seed);
        int64_t pairs = (high * 32768 + next_random(&seed)) % 50000;
        high = next_random(&seed);
        int64_t single = (high * 32768 + next_random(&seed)) % (pairs + 1);
        int64_t *nums = malloc((2 * pairs + 1) * sizeof(int64_t));
        int64_t n = 0, v = 0;
        for (int64_t i = 0; i < pairs + 1; i++) {
            v += 1 + next_random(&seed) % 2;
            nums[n++] = v;
            if (i != single) nums[n++] = v;
        }
        all[t] = nums;
        lens[t] = n;
        elements += n;
    }
    int64_t total = 0, checksum = 0;
    for (int r = 0; r < 200000; r++) {
        for (int64_t t = 0; t < arrays; t++) {
            int64_t answer = single_non_duplicate(all[t], lens[t]);
            total += answer;
            checksum = (checksum * 31 + answer) % 1000000007;
        }
    }
    printf("%lld arrays, %lld elements, 200000 times each: total %lld, checksum %lld\n",
           (long long)arrays, (long long)elements, (long long)total, (long long)checksum);
    return 0;
}
