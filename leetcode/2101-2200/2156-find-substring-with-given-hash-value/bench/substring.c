// LeetCode #2156: Find Substring With Given Hash Value -- the benchmark's
// C mirror of substring.kara. The answer is handed back as its start and
// copied out, as the other languages' slices are.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 20000

static int64_t seed = 2156;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

// writes the k letters of the first window with the hash into out
static void sub_str_hash(const char *s, int64_t n, int64_t power, int64_t modulo, int64_t k, int64_t hash_value, int64_t *letters, char *out) {
    for (int64_t i = 0; i < n; i++) {
        letters[i] = s[i] - 'a' + 1;
    }
    int64_t p = power % modulo;
    int64_t top = 1 % modulo;
    for (int64_t j = 0; j < k; j++) {
        top = top * p % modulo;
    }
    int64_t hash = 0;
    int64_t start = n - k;
    for (int64_t i = n - 1; i >= 0; i--) {
        hash = (hash * p + letters[i]) % modulo;
        if (i + k < n) {
            hash = (hash - letters[i + k] * top % modulo + modulo) % modulo;
        }
        if (i + k <= n && hash == hash_value) {
            start = i;
        }
    }
    memcpy(out, s + start, (size_t)k);
    out[k] = '\0';
}

static int64_t window_hash(const char *s, int64_t start, int64_t k, int64_t power, int64_t modulo) {
    int64_t hash = 0;
    int64_t weight = 1 % modulo;
    for (int64_t j = 0; j < k; j++) {
        hash = (hash + (s[start + j] - 'a' + 1) * weight) % modulo;
        weight = weight * power % modulo;
    }
    return hash;
}

int main(void) {
    char *strings[4];
    for (int t = 0; t < 4; t++) {
        strings[t] = malloc(N + 1);
        for (int64_t i = 0; i < N; i++) {
            strings[t][i] = (char)('a' + next_random() % 26);
        }
        strings[t][N] = '\0';
    }
    int64_t *letters = malloc(N * sizeof(int64_t));
    char *found = malloc(N + 1);
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t round = 0; round < 50; round++) {
        for (int t = 0; t < 4; t++) {
            int64_t at = next_random() % N;
            strings[t][at] = (char)('a' + next_random() % 26);
            int64_t k = next_random() % N + 1;
            int64_t power = 1000000000 - next_random();
            int64_t modulo = 1000000000 - next_random();
            int64_t start = next_random() % (N - k + 1);
            int64_t hash_value = window_hash(strings[t], start, k, power, modulo);
            sub_str_hash(strings[t], N, power, modulo, k, hash_value, letters, found);
            total += k;
            check = (check * 31 + k + found[0] + found[k - 1] + round) % 1000000007;
        }
    }
    printf("200 solves: %lld letters in all, checksum %lld\n", (long long)total, (long long)check);
    for (int t = 0; t < 4; t++) {
        free(strings[t]);
    }
    free(letters);
    free(found);
    return 0;
}
