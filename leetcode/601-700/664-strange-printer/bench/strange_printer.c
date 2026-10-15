// Benchmark for #664: intervals, by their last letter, as the Kara ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t strange_printer(const char *s) {
    int64_t n = (int64_t)strlen(s);
    if (n == 0) {
        return 0;
    }
    int64_t *turns = calloc((size_t)(n * n), sizeof(int64_t));
    for (int64_t i = n - 1; i >= 0; i--) {
        turns[i * n + i] = 1;
        for (int64_t j = i + 1; j < n; j++) {
            int64_t best = turns[i * n + j - 1] + 1;
            for (int64_t k = i; k < j; k++) {
                if (s[k] == s[j]) {
                    int64_t between = k + 1 <= j - 1 ? turns[(k + 1) * n + j - 1] : 0;
                    int64_t t = turns[i * n + k] + between;
                    if (t < best) {
                        best = t;
                    }
                }
            }
            turns[i * n + j] = best;
        }
    }
    int64_t answer = turns[n - 1];
    free(turns);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 664;
    char texts[64][101];
    for (int t = 0; t < 64; t++) {
        int64_t letters = 2 + t % 25;
        for (int i = 0; i < 100; i++) {
            texts[t][i] = (char)(97 + next_random(&seed) % letters);
        }
        texts[t][100] = 0;
    }
    int64_t rounds = 2000;
    int64_t sum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t t = strange_printer(texts[r % 64]);
        sum = (sum * 31 + t + r) % 1000000007;
    }
    printf("64 texts of 100 letters, %lld rounds: checksum %lld\n", (long long)rounds, (long long)sum);
    return 0;
}
