// Benchmark for #466: mirror of count_repetitions.kara (the ★ arm: find
// the cycle) on the same workload. C has no map; a position in s2 is
// below |s2|, so the memo of positions is an array indexed by it,
// cleared per call.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t get_max_repetitions(const char *a, int64_t alen, int64_t n1, const char *b, int64_t blen,
                                   int64_t n2) {
    int64_t index = 0;
    int64_t count = 0;
    int64_t *seen_k = malloc(blen * sizeof(int64_t));
    int64_t *seen_count = malloc(blen * sizeof(int64_t));
    for (int64_t i = 0; i < blen; i++) {
        seen_k[i] = -1;
    }
    int64_t k = 0;
    while (k < n1) {
        for (int64_t i = 0; i < alen; i++) {
            if (a[i] == b[index]) {
                index += 1;
                if (index == blen) {
                    index = 0;
                    count += 1;
                }
            }
        }
        k += 1;
        if (seen_k[index] >= 0) {
            int64_t cycle = k - seen_k[index];
            int64_t cycles = (n1 - k) / cycle;
            count += cycles * (count - seen_count[index]);
            k += cycles * cycle;
            while (k < n1) {
                for (int64_t i = 0; i < alen; i++) {
                    if (a[i] == b[index]) {
                        index += 1;
                        if (index == blen) {
                            index = 0;
                            count += 1;
                        }
                    }
                }
                k += 1;
            }
            break;
        }
        seen_k[index] = k;
        seen_count[index] = count;
    }
    free(seen_k);
    free(seen_count);
    return count / n2;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    enum { PAIRS = 100 };
    const int64_t rounds = 1000;
    int64_t seed = 466;
    char firsts[PAIRS][100];
    char seconds[PAIRS][100];
    int64_t second_len[PAIRS];
    for (int p = 0; p < PAIRS; p++) {
        for (int i = 0; i < 100; i++) {
            firsts[p][i] = (char)(97 + next_random(&seed) % 26);
        }
        second_len[p] = 1 + next_random(&seed) % 100;
        for (int64_t i = 0; i < second_len[p]; i++) {
            seconds[p][i] = firsts[p][next_random(&seed) % 100];
        }
    }
    int64_t total = 0;
    int64_t checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int p = 0; p < PAIRS; p++) {
            int64_t hi = next_random(&seed);
            int64_t lo = next_random(&seed);
            int64_t n1 = 1 + (hi * 32768 + lo) % 1000000;
            int64_t n2 = 1 + next_random(&seed) % 100;
            int64_t m = get_max_repetitions(firsts[p], 100, n1, seconds[p], second_len[p], n2);
            total += m;
            checksum = (checksum * 31 + m) % 1000000007;
        }
    }
    printf("%lld rounds on %d pairs: %lld repetitions in all, checksum %lld\n", (long long)rounds, PAIRS,
           (long long)total, (long long)checksum);
    return 0;
}
