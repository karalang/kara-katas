// Benchmark for #665: fix each drop as it comes, as the Kara ★ arm.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static bool check_possibility(const int64_t *nums, size_t n) {
    int64_t *a = malloc(n * sizeof(int64_t));
    memcpy(a, nums, n * sizeof(int64_t));
    int fixes = 0;
    bool ok = true;
    for (size_t i = 1; i < n; i++) {
        if (a[i] < a[i - 1]) {
            fixes++;
            if (fixes > 1) {
                ok = false;
                break;
            }
            if (i < 2 || a[i - 2] <= a[i]) {
                a[i - 1] = a[i];
            } else {
                a[i] = a[i - 1];
            }
        }
    }
    free(a);
    return ok;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 665;
    static int64_t arrays[16][10000];
    for (int t = 0; t < 16; t++) {
        int64_t x = -100000;
        for (int i = 0; i < 10000; i++) {
            arrays[t][i] = x;
            x += next_random(&seed) % 21;
        }
        for (int k = 0; k < t % 3; k++) {
            int64_t at = next_random(&seed) % 10000;
            arrays[t][at] = next_random(&seed) % 200001 - 100000;
        }
    }
    int64_t rounds = 40000;
    int64_t yes = 0;
    int64_t sum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        bool ok = check_possibility(arrays[r % 16], 10000);
        if (ok) {
            yes++;
        }
        sum = (sum * 31 + r * 2 + (ok ? 1 : 0)) % 1000000007;
    }
    printf("16 arrays of 10000, %lld rounds: %lld can be sorted, checksum %lld\n", (long long)rounds,
           (long long)yes, (long long)sum);
    return 0;
}
