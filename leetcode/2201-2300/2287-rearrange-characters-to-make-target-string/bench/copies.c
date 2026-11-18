// LeetCode #2287: Rearrange Characters to Make Target String -- the
// bench, the ★ arm's C twin. Two arrays of 26 counts and the least
// quotient; the strings are NUL-terminated.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t rearrange_characters(const char *s, const char *target) {
    int64_t have[26] = {0}, need[26] = {0};
    int64_t n = 0;
    for (const char *p = s; *p; p++, n++) have[*p - 'a']++;
    for (const char *p = target; *p; p++) need[*p - 'a']++;
    int64_t copies = n;
    for (int i = 0; i < 26; i++) {
        if (need[i] > 0 && have[i] / need[i] < copies) copies = have[i] / need[i];
    }
    return copies;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2287;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static void word(char *out, int64_t len, int64_t letters) {
    for (int64_t i = 0; i < len; i++) out[i] = (char)('a' + next_random() % letters);
    out[len] = '\0';
}

int main(void) {
    static char ss[10000][101], ts[10000][11];
    for (int i = 0; i < 10000; i++) {
        int64_t letters = next_random() % 6 + 1;
        int64_t s_len = next_random() % 100 + 1;
        int64_t t_len = next_random() % 10 + 1;
        word(ss[i], s_len, letters);
        word(ts[i], t_len, letters);
    }
    int64_t check = 0;
    for (int p = 0; p < 200; p++) {
        int64_t total = 0;
        for (int i = 0; i < 10000; i++) total += rearrange_characters(ss[i], ts[i]);
        check = (check * 31 + total) % 1000000007;
    }
    printf("200 passes over 10^4 pairs: checksum %lld\n", (long long)check);
    return 0;
}
