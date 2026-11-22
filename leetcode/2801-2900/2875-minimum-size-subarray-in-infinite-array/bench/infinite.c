// LeetCode #2875: Minimum Size Subarray in Infinite Array -- the bench,
// as infinite.kara: 50 arrays of 10^5 values, each with its target,
// answered 20 times by the sliding-window arm.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t min_size_subarray(const int64_t *nums, int64_t n, int64_t target) {
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) total += nums[i];
    int64_t whole = target / total * n, rest = target % total;
    if (rest == 0) return whole;
    int64_t best = -1, sum = 0, left = 0;
    for (int64_t right = 0; right < 2 * n; right++) {
        sum += nums[right % n];
        while (sum > rest) {
            sum -= nums[left % n];
            left++;
        }
        if (sum == rest && (best < 0 || right - left + 1 < best)) best = right - left + 1;
    }
    return best < 0 ? -1 : whole + best;
}

static int64_t seed = 2875;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int64_t count = 50, rounds = 20, n = 100000;
    int64_t *arrays = malloc(count * n * sizeof *arrays);
    int64_t targets[50];
    for (int64_t c = 0; c < count; c++) {
        int64_t top = c % 2 == 1 ? 10 : 100000;
        for (int64_t i = 0; i < n; i++) arrays[c * n + i] = wide() % top + 1;
        targets[c] = wide() % 1000000000 + 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t length = min_size_subarray(arrays + c * n, n, targets[c]);
            total += length;
            check = (check * 31 + length + 1 + r) % 1000000007;
        }
    }
    printf("%lld arrays of %lld, %lld rounds: lengths total %lld, checksum %lld\n", (long long)count, (long long)n,
           (long long)rounds, (long long)total, (long long)check);
    free(arrays);
    return 0;
}
