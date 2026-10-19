// Benchmark for #775: Global and Local Inversions -- the ★ arm (every
// value at most one place from its index), as the Kāra program does it.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static bool is_ideal_permutation(const int64_t *nums, int64_t n) {
    for (int64_t i = 0; i < n; i++) {
        int64_t d = nums[i] - i;
        if (d > 1 || d < -1) {
            return false;
        }
    }
    return true;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static void swap(int64_t *nums, int64_t a, int64_t b) {
    int64_t t = nums[a];
    nums[a] = nums[b];
    nums[b] = t;
}

int main(void) {
    const int64_t count = 64, n = 100000;
    int64_t seed = 775;
    int64_t *perms[64];
    for (int64_t g = 0; g < count; g++) {
        int64_t *nums = malloc(sizeof(int64_t) * n);
        for (int64_t v = 0; v < n; v++) {
            nums[v] = v;
        }
        int64_t i = 0;
        while (i + 1 < n) {
            if (next_random(&seed) % 2 == 0) {
                swap(nums, i, i + 1);
                i += 2;
            } else {
                i += 1;
            }
        }
        if (g % 4 == 1) {
            int64_t at = n - 4 - next_random(&seed) % 1000;
            swap(nums, at, at + 3);
        } else if (g % 4 == 2) {
            int64_t at = next_random(&seed) % (n - 3);
            swap(nums, at, at + 3);
        }
        perms[g] = nums;
    }
    int64_t ideals = 0, checksum = 0;
    for (int64_t round = 0; round < 12000; round++) {
        int64_t g = (round * 7) % count;
        if (is_ideal_permutation(perms[g], n)) {
            ideals++;
            checksum = (checksum * 31 + g + 1) % 1000000007;
        } else {
            checksum = (checksum * 31 + 7) % 1000000007;
        }
    }
    printf("12000 rounds of %lld values: %lld ideal, checksum %lld\n", (long long)n, (long long)ideals,
           (long long)checksum);
    for (int64_t g = 0; g < count; g++) {
        free(perms[g]);
    }
    return 0;
}
