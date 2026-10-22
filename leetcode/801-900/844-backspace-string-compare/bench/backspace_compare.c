// Benchmark for #844: Backspace String Compare -- C twin of the Kāra ★ arm
// (two pointers from the back).
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>

// the index of the last surviving character at or before `i`, or -1
static int64_t next_kept(const char *s, int64_t i) {
    int64_t skip = 0;
    while (i >= 0) {
        if (s[i] == '#') {
            skip++;
        } else if (skip > 0) {
            skip--;
        } else {
            return i;
        }
        i--;
    }
    return -1;
}

static bool backspace_compare(const char *a, const char *b) {
    int64_t i = next_kept(a, (int64_t)strlen(a) - 1);
    int64_t j = next_kept(b, (int64_t)strlen(b) - 1);
    while (i >= 0 && j >= 0) {
        if (a[i] != b[j]) return false;
        i = next_kept(a, i - 1);
        j = next_kept(b, j - 1);
    }
    return i < 0 && j < 0;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 64, rounds = 3500000;
    int64_t seed = 844;
    static char firsts[64][256], seconds[64][256];
    for (int64_t g = 0; g < count; g++) {
        int64_t k = 2 + g % 3;
        char cs[256];
        int64_t len = 0;
        for (int i = 0; i < 120; i++) {
            if (next_random(&seed) % 10 < 3) cs[len++] = '#';
            else cs[len++] = (char)(97 + next_random(&seed) % k);
        }
        memcpy(firsts[g], cs, (size_t)len);
        firsts[g][len] = 0;
        for (int e = 0; e < 40; e++) {
            int64_t at = next_random(&seed) % (len + 1);
            memmove(cs + at + 1, cs + at, (size_t)(len - at));
            cs[at] = '#';
            len++;
            memmove(cs + at + 1, cs + at, (size_t)(len - at));
            cs[at] = (char)(97 + next_random(&seed) % k);
            len++;
        }
        if (g % 2 == 1) {
            int64_t at = next_random(&seed) % len;
            cs[at] = cs[at] == '#' ? 'a' : '#';
        }
        memcpy(seconds[g], cs, (size_t)len);
        seconds[g][len] = 0;
    }
    int64_t equal = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t g = round % count;
        bool same = backspace_compare(firsts[g], seconds[g]);
        if (same) equal++;
        checksum = (checksum * 31 + (same ? round % 1000 : 7)) % 1000000007;
    }
    printf("%lld rounds of %lld pairs: %lld equal, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)equal, (long long)checksum);
    return 0;
}
