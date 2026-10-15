// Benchmark for #674: one pass with a running length, as the Kara ★
// arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t find_length_of_lcis(const int64_t *nums, int64_t n) {
    int64_t best = 0;
    int64_t run = 0;
    for (int64_t i = 0; i < n; i++) {
        if (i > 0 && nums[i - 1] < nums[i]) {
            run += 1;
        } else {
            run = 1;
        }
        if (run > best) best = run;
    }
    return best;
}

int main(void) {
    int64_t arrays = 100;
    int64_t size = 10000;
    int64_t rounds = 20000;
    int64_t seed = 674;
    int64_t **all = malloc(sizeof(int64_t *) * arrays);
    for (int64_t a = 0; a < arrays; a++) {
        all[a] = malloc(sizeof(int64_t) * size);
        for (int64_t i = 0; i < size; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            all[a][i] = seed / 65536 % 1000;
        }
    }
    int64_t sum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t *nums = all[r % arrays];
        nums[r * 7919 % size] = r % 1000;
        sum = (sum * 31 + find_length_of_lcis(nums, size)) % 1000000007;
    }
    for (int64_t a = 0; a < arrays; a++) free(all[a]);
    free(all);
    printf("%lld rounds over %lld arrays of %lld: checksum %lld\n", (long long)rounds,
           (long long)arrays, (long long)size, (long long)sum);
    return 0;
}
