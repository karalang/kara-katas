// Benchmark for #673: the length and count ending at each place, as the
// Kara ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t find_number_of_lis(const int64_t *nums, int64_t n) {
    int64_t *length = malloc(sizeof(int64_t) * n);
    int64_t *count = malloc(sizeof(int64_t) * n);
    for (int64_t i = 0; i < n; i++) {
        length[i] = 1;
        count[i] = 1;
    }
    for (int64_t i = 0; i < n; i++) {
        for (int64_t j = 0; j < i; j++) {
            if (nums[j] < nums[i]) {
                if (length[j] + 1 > length[i]) {
                    length[i] = length[j] + 1;
                    count[i] = count[j];
                } else if (length[j] + 1 == length[i]) {
                    count[i] += count[j];
                }
            }
        }
    }
    int64_t best = 0;
    for (int64_t i = 0; i < n; i++) {
        if (length[i] > best) best = length[i];
    }
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        if (length[i] == best) total += count[i];
    }
    free(length);
    free(count);
    return total;
}

int main(void) {
    int64_t rounds = 150;
    int64_t size = 2000;
    int64_t seed = 673;
    int64_t sum = 0;
    int64_t *nums = malloc(sizeof(int64_t) * size);
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < size; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            nums[i] = seed / 65536;
        }
        sum = (sum * 31 + find_number_of_lis(nums, size)) % 1000000007;
    }
    free(nums);
    printf("%lld arrays of %lld: checksum %lld\n", (long long)rounds, (long long)size, (long long)sum);
    return 0;
}
