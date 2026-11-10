// Benchmark: LeetCode #1100 Find K-Length Substrings With No Repeated
// Characters -- the sliding window with a count of each letter, as the
// Kāra ★ arm. 64 texts of 10^4 letters are built once; each of 10 rounds
// changes one letter in every text and counts its substrings for 4 values
// of k from 1 to 30. Each round joins the text into a fresh string and
// each count takes its own copy, as the Kāra and Rust benches do.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 10000

static int64_t num_k_len_substr_no_repeats(const char *b, int64_t len, int64_t k) {
    if (k > 26 || k > len) return 0;
    int64_t count[26] = {0};
    int64_t repeated = 0, found = 0;
    for (int64_t i = 0; i < len; i++) {
        int c = b[i] - 'a';
        if (++count[c] == 2) repeated++;
        if (i >= k) {
            int out = b[i - k] - 'a';
            if (--count[out] == 1) repeated--;
        }
        if (i >= k - 1 && repeated == 0) found++;
    }
    return found;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1100;
    static char texts[64][N];
    for (int64_t j = 0; j < 64; j++) {
        int64_t alphabet = 8 + j % 19;
        for (int i = 0; i < N; i++) texts[j][i] = (char)('a' + next_random(&seed) % alphabet);
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 10; round++) {
        for (int64_t j = 0; j < 64; j++) {
            int64_t at = (round * 7919 + j * 104729) % N;
            texts[j][at] = (char)('a' + (round + j) % 26);
            char *s = malloc(N);
            memcpy(s, texts[j], N);
            for (int64_t q = 0; q < 4; q++) {
                int64_t k = (round * 7 + j * 3 + q * 11) % 30 + 1;
                char *copy = malloc(N);
                memcpy(copy, s, N);
                int64_t count = num_k_len_substr_no_repeats(copy, N, k);
                free(copy);
                total += count;
                check = (check * 31 + count + 1) % 1000000007;
            }
            free(s);
        }
    }
    printf("10 rounds over 64 texts of 10^4 letters: %lld substrings, checksum %lld\n",
           (long long)total, (long long)check);
    return 0;
}
