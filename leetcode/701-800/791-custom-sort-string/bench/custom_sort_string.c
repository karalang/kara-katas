// LeetCode 791 — Custom Sort String: the bench, in C.
// Mirrors custom_sort_string.kara: count the letters, write out order's
// letters, then the rest in place, into a new buffer each round.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *custom_sort_string(const char *order, const char *s) {
    int64_t count[26] = {0};
    int named[26] = {0};
    size_t n = strlen(s);
    for (size_t i = 0; i < n; i++) count[s[i] - 'a']++;
    char *out = malloc(n + 1);
    size_t len = 0;
    for (const char *c = order; *c; c++) {
        int at = *c - 'a';
        named[at] = 1;
        for (int64_t k = 0; k < count[at]; k++) out[len++] = *c;
    }
    for (size_t i = 0; i < n; i++)
        if (!named[s[i] - 'a']) out[len++] = s[i];
    out[len] = 0;
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const char *letters = "abcdefghijklmnopqrstuvwxyz";
    int64_t seed = 791;
    static char orders[64][27];
    static char strings[64][201];
    for (int k = 0; k < 64; k++) {
        char pool[26];
        memcpy(pool, letters, 26);
        for (int64_t i = 25; i > 0; i--) {
            int64_t j = next_random(&seed) % (i + 1);
            char t = pool[i];
            pool[i] = pool[j];
            pool[j] = t;
        }
        int64_t size = 1 + next_random(&seed) % 26;
        memcpy(orders[k], pool, size);
        orders[k][size] = 0;
        for (int i = 0; i < 200; i++) strings[k][i] = letters[next_random(&seed) % 26];
        strings[k][200] = 0;
    }
    int64_t rounds = 1000000, total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        char *answer = custom_sort_string(orders[r % 64], strings[(r / 64) % 64]);
        size_t len = strlen(answer);
        total += len;
        if (r % 1000 == 0)
            for (size_t i = 0; i < len; i++) check = (check * 131 + (unsigned char)answer[i]) % 1000000007;
        free(answer);
    }
    printf("%lld rounds of 200-letter strings: %lld letters, checksum %lld\n", (long long)rounds, (long long)total,
           (long long)check);
    return 0;
}
