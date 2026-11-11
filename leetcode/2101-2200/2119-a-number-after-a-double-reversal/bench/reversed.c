// LeetCode #2119: A Number After a Double Reversal -- the benchmark, the
// same algorithm as reversed.kara: each number's digits reversed by % 10
// and / 10, twice.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t reverse(int64_t num) {
    int64_t n = num, out = 0;
    while (n > 0) {
        out = out * 10 + n % 10;
        n /= 10;
    }
    return out;
}

static bool is_same_after_reversals(int64_t num) {
    return reverse(reverse(num)) == num;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 2119;
    const int64_t n = 1000000;
    int64_t *nums = malloc(n * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        int64_t num = next_random(&seed) % 1000001;
        if (next_random(&seed) % 3 == 0) {
            num = num / 1000 * 1000;
        }
        nums[i] = num;
    }
    int64_t same = 0, check = 0;
    for (int64_t round = 0; round < 100; round++) {
        nums[round * 7919 % n] += 1;
        for (int64_t i = 0; i < n; i++) {
            if (is_same_after_reversals(nums[i])) {
                same++;
                check = (check * 31 + nums[i] % 1000) % 1000000007;
            }
        }
    }
    printf("100000000 checks: %lld the same, checksum %lld\n", (long long)same, (long long)check);
    free(nums);
    return 0;
}
