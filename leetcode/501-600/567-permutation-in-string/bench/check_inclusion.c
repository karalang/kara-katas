// Benchmark for #567: C mirror of the ★ arm (a sliding window); see
// check_inclusion.kara. Each call copies both texts into fresh arrays of
// code points, as the Kāra arm collects each String's chars into a Vec.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static uint32_t *to_chars(const char *s, int64_t *len) {
    int64_t n = (int64_t)strlen(s);
    uint32_t *out = malloc((size_t)(n > 0 ? n : 1) * sizeof(uint32_t));
    for (int64_t i = 0; i < n; i++) {
        out[i] = (unsigned char)s[i];
    }
    *len = n;
    return out;
}

static int check_inclusion(const char *s1, const char *s2) {
    int64_t k, n;
    uint32_t *a = to_chars(s1, &k);
    uint32_t *b = to_chars(s2, &n);
    int result = 0;
    if (k > n) {
        free(a);
        free(b);
        return 0;
    }
    int64_t need[26] = {0};
    for (int64_t i = 0; i < k; i++) {
        need[a[i] - 'a'] += 1;
    }
    int64_t missing = k;
    for (int64_t i = 0; i < n; i++) {
        int64_t enter = (int64_t)b[i] - 'a';
        if (need[enter] > 0) {
            missing -= 1;
        }
        need[enter] -= 1;
        if (i >= k) {
            int64_t leave = (int64_t)b[i - k] - 'a';
            need[leave] += 1;
            if (need[leave] > 0) {
                missing += 1;
            }
        }
        if (missing == 0) {
            result = 1;
            break;
        }
    }
    free(a);
    free(b);
    return result;
}

// ---- benchmark --------------------------------------------------------------

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static char *random_text(int64_t length, int64_t letters, int64_t *seed) {
    const char *alphabet = "abcdefghijklmnopqrstuvwxyz";
    char *s = malloc((size_t)length + 1);
    for (int64_t i = 0; i < length; i++) {
        s[i] = alphabet[step(seed) % letters];
    }
    s[length] = '\0';
    return s;
}

int main(void) {
    int64_t count = 100;
    int64_t rounds = 300;
    int64_t seed = 567;
    char *s1s[100];
    char *s2s[100];
    for (int64_t g = 0; g < count; g++) {
        int64_t letters = 3 + step(&seed) % 24;
        int64_t len1 = 5 + step(&seed) % 196;
        char *s1 = random_text(len1, letters, &seed);
        char *s2 = random_text(10000, letters, &seed);
        if (g % 2 == 0) {
            char *shuffled = malloc((size_t)len1 + 1);
            memcpy(shuffled, s1, (size_t)len1 + 1);
            int64_t i = len1 - 1;
            while (i > 0) {
                int64_t j = step(&seed) % (i + 1);
                char t = shuffled[i];
                shuffled[i] = shuffled[j];
                shuffled[j] = t;
                i -= 1;
            }
            int64_t cut = step(&seed) % (10001 - len1);
            memcpy(s2 + cut, shuffled, (size_t)len1);
            free(shuffled);
        }
        s1s[g] = s1;
        s2s[g] = s2;
    }
    int64_t found = 0;
    int64_t checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int64_t g = 0; g < count; g++) {
            int64_t p = (round * 7 + g) % count;
            int got = check_inclusion(s1s[p], s2s[p]);
            if (got) {
                found += 1;
            }
            checksum = (checksum * 31 + (got ? g + 2 : 1)) % 1000000007;
        }
    }
    printf("%lld pairs, %lld rounds: %lld found, checksum %lld\n", (long long)count,
           (long long)rounds, (long long)found, (long long)checksum);
    for (int64_t g = 0; g < count; g++) {
        free(s1s[g]);
        free(s2s[g]);
    }
    return 0;
}
