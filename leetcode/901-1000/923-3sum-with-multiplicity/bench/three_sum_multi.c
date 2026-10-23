// LeetCode #923: 3Sum With Multiplicity -- bench: counting the values.
// Mirrors three_sum_multi.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t three_sum_multi(const int64_t *arr, int64_t len, int64_t target) {
    const int64_t modulus = 1000000007;
    int64_t count[101] = {0};
    for (int64_t i = 0; i < len; i++) count[arr[i]]++;
    int64_t total = 0;
    for (int64_t x = 0; x < 101; x++) {
        if (3 * x > target) break;
        for (int64_t y = x; y < 101; y++) {
            int64_t z = target - x - y;
            if (z < y) break;
            if (z > 100) continue;
            int64_t ways;
            if (x == y && y == z) ways = count[x] * (count[x] - 1) * (count[x] - 2) / 6;
            else if (x == y) ways = count[x] * (count[x] - 1) / 2 * count[z];
            else if (y == z) ways = count[x] * count[y] * (count[y] - 1) / 2;
            else ways = count[x] * count[y] * count[z];
            total = (total + ways) % modulus;
        }
    }
    return total;
}

static int64_t seed = 923;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t rounds = 500, count = 100, n = 3000;
    // count arrays of n values from 0 to 100, built once
    int64_t **arrays = malloc(count * sizeof(int64_t *));
    for (int64_t i = 0; i < count; i++) {
        arrays[i] = malloc(n * sizeof(int64_t));
        for (int64_t j = 0; j < n; j++) arrays[i][j] = next_random() % 101;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        // each round asks every array for a different target up to 300
        for (int64_t i = 0; i < count; i++) {
            int64_t a = three_sum_multi(arrays[i], n, (r * 7 + i) % 301);
            total += a;
            check = (check * 1000003 + a) % 1000000007;
        }
    }
    printf("%lld rounds over %lld arrays of %lld: answers summing to %lld, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)n, (long long)total, (long long)check);
    for (int64_t i = 0; i < count; i++) free(arrays[i]);
    free(arrays);
    return 0;
}
