// Benchmark for #848: Shifting Letters -- C twin of the Kāra ★ arm (suffix
// sums, from the back).
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define N 100000

static char *shifting_letters(const char *s, const int64_t *shifts, int64_t n) {
    char *out = malloc((size_t)n + 1);
    memcpy(out, s, (size_t)n + 1);
    int64_t shift = 0;
    for (int64_t i = n - 1; i >= 0; i--) {
        shift = (shift + shifts[i]) % 26;
        out[i] = (char)('a' + (out[i] - 'a' + shift) % 26);
    }
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 64, rounds = 2000, n = N;
    int64_t seed = 848;
    static char texts[64][N + 1];
    static int64_t shifts[64][N];
    for (int64_t g = 0; g < count; g++) {
        for (int64_t i = 0; i < n; i++) {
            texts[g][i] = (char)('a' + next_random(&seed) % 26);
            shifts[g][i] = next_random(&seed) * 4657 % 1000000001;
        }
        texts[g][n] = 0;
    }
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        char *out = shifting_letters(texts[round % count], shifts[round % count], n);
        checksum = (checksum * 31 + out[0] + out[n / 2] * 7 + out[n - 1] * 13) % 1000000007;
        free(out);
    }
    printf("%lld rounds of %lld strings: checksum %lld\n", (long long)rounds, (long long)count,
           (long long)checksum);
    return 0;
}
