// Benchmark for #565: C mirror of the ★ arm (walk each cycle once); see
// array_nesting.kara. The marks are a fresh `calloc`'d array per answer,
// as the Kāra arm's are a fresh vector.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t array_nesting(const int64_t *nums, int64_t n) {
    bool *visited = calloc(n, sizeof(bool));
    int64_t best = 0;
    for (int64_t start = 0; start < n; start++) {
        if (visited[start]) continue;
        int64_t length = 0;
        int64_t i = start;
        while (!visited[i]) {
            visited[i] = true;
            i = nums[i];
            length += 1;
        }
        if (length > best) best = length;
    }
    free(visited);
    return best;
}

// ---- benchmark --------------------------------------------------------------

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t count = 20;
    int64_t rounds = 100;
    int64_t n = 100000;
    int64_t seed = 565;
    int64_t **perms = malloc(count * sizeof(int64_t *));
    for (int64_t g = 0; g < count; g++) {
        int64_t *nums = malloc(n * sizeof(int64_t));
        for (int64_t i = 0; i < n; i++) nums[i] = i;
        if (g % 2 == 0) {
            for (int64_t i = n - 1; i > 0; i--) {
                int64_t hi = step(&seed);
                int64_t j = (hi * 32768 + step(&seed)) % (i + 1);
                int64_t t = nums[i];
                nums[i] = nums[j];
                nums[j] = t;
            }
        } else {
            int64_t start = 0;
            while (start < n) {
                int64_t length = 1 + step(&seed) % 2000;
                if (length > n - start) length = n - start;
                for (int64_t j = 0; j < length; j++) nums[start + j] = start + (j + 1) % length;
                start += length;
            }
        }
        perms[g] = nums;
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int64_t g = 0; g < count; g++) {
            int64_t got = array_nesting(perms[(round * 7 + g) % count], n);
            total += got;
            checksum = (checksum * 31 + got) % 1000000007;
        }
    }
    printf("%lld permutations of %lld, %lld rounds: total %lld, checksum %lld\n", (long long)count,
           (long long)n, (long long)rounds, (long long)total, (long long)checksum);
    for (int64_t g = 0; g < count; g++) free(perms[g]);
    free(perms);
    return 0;
}
