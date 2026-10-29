// LeetCode #1013: Partition Array Into Three Parts With Equal Sum -- bench
// Mirrors three_parts.kara; see ../README.md § Benchmarks.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static bool can_three_parts_equal_sum(const int64_t *arr, int64_t n) {
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        total += arr[i];
    }
    if (total % 3 != 0) {
        return false;
    }
    int64_t target = total / 3;
    int64_t prefix = 0;
    int cuts = 0;
    for (int64_t i = 0; i < n - 1; i++) {
        prefix += arr[i];
        if (cuts == 0 && prefix == target) {
            cuts = 1;
        } else if (cuts == 1 && prefix == 2 * target) {
            return true;
        }
    }
    return false;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t count = 50000;
    int64_t rounds = 10000;
    int64_t seed = 1013;
    int64_t *arr = malloc(count * sizeof(int64_t));
    int64_t total = 0;
    for (int64_t i = 0; i < count; i++) {
        int64_t x = next_random(&seed) % 7 - 2;
        arr[i] = x;
        total += x;
    }
    arr[count - 1] -= total % 3;
    int64_t yes = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t hi = next_random(&seed);
        int64_t lo = next_random(&seed);
        int64_t at = (hi * 32768 + lo) % count;
        arr[at] += 3 * (next_random(&seed) % 3 - 1);
        bool answer = can_three_parts_equal_sum(arr, count);
        if (answer) {
            yes++;
        }
        check = (check * 2 + (answer ? 1 : 0)) % 1000000007;
    }
    printf("%lld rounds over %lld values: %lld split, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)yes, (long long)check);
    free(arr);
    return 0;
}
