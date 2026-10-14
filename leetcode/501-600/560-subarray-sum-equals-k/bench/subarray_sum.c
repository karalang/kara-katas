// Benchmark for #560: C mirror of the ★ arm (prefix sums in a hash map);
// see subarray_sum.kara. C has no hash map, so this one is open
// addressing with linear probing, a fresh table per call sized to twice
// the most distinct prefix sums.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t key;
    int64_t value;
    int used;
} Slot;

static size_t find(Slot *table, size_t mask, int64_t key) {
    size_t i = (size_t)((uint64_t)key * 0x9E3779B97F4A7C15ull >> 32) & mask;
    while (table[i].used && table[i].key != key) {
        i = (i + 1) & mask;
    }
    return i;
}

static int64_t subarray_sum(const int64_t *nums, size_t n, int64_t k) {
    size_t size = 1;
    while (size < 2 * (n + 1)) {
        size *= 2;
    }
    size_t mask = size - 1;
    Slot *seen = calloc(size, sizeof(Slot));
    size_t z = find(seen, mask, 0);
    seen[z].used = 1;
    seen[z].key = 0;
    seen[z].value = 1;
    int64_t sum = 0;
    int64_t count = 0;
    for (size_t i = 0; i < n; i++) {
        sum += nums[i];
        size_t j = find(seen, mask, sum - k);
        if (seen[j].used) {
            count += seen[j].value;
        }
        size_t s = find(seen, mask, sum);
        if (!seen[s].used) {
            seen[s].used = 1;
            seen[s].key = sum;
            seen[s].value = 0;
        }
        seen[s].value += 1;
    }
    free(seen);
    return count;
}

// ---- benchmark --------------------------------------------------------------

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 100;
    const int64_t n = 20000;
    const int64_t rounds = 20;
    int64_t seed = 560;
    int64_t **arrays = malloc(count * sizeof(int64_t *));
    for (int64_t a = 0; a < count; a++) {
        arrays[a] = malloc(n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) {
            arrays[a][i] = step(&seed) % 2001 - 1000;
        }
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int64_t g = 0; g < count; g++) {
            int64_t k = step(&seed) % 2001 - 1000;
            int64_t c = subarray_sum(arrays[(round * 7 + g) % count], (size_t)n, k);
            total += c;
            checksum = (checksum * 31 + c) % 1000000007;
        }
    }
    printf("%lld arrays of %lld, %lld rounds: %lld subarrays, checksum %lld\n",
           (long long)count, (long long)n, (long long)rounds, (long long)total, (long long)checksum);
    for (int64_t a = 0; a < count; a++) {
        free(arrays[a]);
    }
    free(arrays);
    return 0;
}
