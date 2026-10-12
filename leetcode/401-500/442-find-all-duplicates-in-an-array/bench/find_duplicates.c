// Benchmark for #442: mirror of find_duplicates.kara (marking by sign) on
// one random array of 1,000,000 numbers with 300,000 duplicates, built
// once, copied and searched 20 times over.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t random_index(int64_t *seed, int64_t below) {
    int64_t a = next_random(seed);
    return (a * 32768 + next_random(seed)) % below;
}

// Writes the duplicates into `out` and returns how many there are.
static int64_t find_duplicates(int64_t *nums, int64_t n, int64_t *out) {
    int64_t count = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t x = llabs(nums[i]);
        if (nums[x - 1] < 0) {
            out[count++] = x;
        } else {
            nums[x - 1] = -nums[x - 1];
        }
    }
    return count;
}

static void swap(int64_t *a, int64_t i, int64_t j) {
    int64_t t = a[i];
    a[i] = a[j];
    a[j] = t;
}

int main(void) {
    const int64_t n = 1000000, d = 300000, rounds = 20;
    int64_t seed = 442;
    int64_t *values = malloc(n * sizeof(int64_t));
    for (int64_t x = 1; x <= n; x++) {
        values[x - 1] = x;
    }
    for (int64_t i = 0; i < n; i++) {
        swap(values, i, i + random_index(&seed, n - i));
    }
    int64_t *nums = malloc(n * sizeof(int64_t));
    int64_t len = 0;
    for (int64_t i = 0; i < n - d; i++) {
        nums[len++] = values[i];
    }
    for (int64_t i = 0; i < d; i++) {
        nums[len++] = values[i];
    }
    for (int64_t i = 0; i < n; i++) {
        swap(nums, i, i + random_index(&seed, n - i));
    }
    int64_t found = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t *copy = malloc(n * sizeof(int64_t));
        memcpy(copy, nums, n * sizeof(int64_t));
        int64_t *duplicates = malloc(n * sizeof(int64_t));
        int64_t count = find_duplicates(copy, n, duplicates);
        found += count;
        for (int64_t i = 0; i < count; i++) {
            checksum = (checksum * 31 + duplicates[i] + round) % 1000000007;
        }
        free(duplicates);
        free(copy);
    }
    printf("%lld rounds on %lld numbers: %lld duplicates, checksum %lld\n", (long long)rounds, (long long)n,
           (long long)found, (long long)checksum);
    free(nums);
    free(values);
    return 0;
}
