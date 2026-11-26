// LeetCode #1763: Longest Nice Substring -- the bench in C, mirroring
// longest_nice_substring.kara: divide and conquer at each letter whose
// other case is missing, each part copied into a new string as the Kāra
// arm's slices are.
#include <ctype.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *copy(const char *s, size_t n) {
    char *t = malloc(n + 1);
    memcpy(t, s, n);
    t[n] = 0;
    return t;
}

// takes ownership of s
static char *longest_nice_substring(char *s) {
    size_t n = strlen(s);
    for (size_t i = 0; i < n; i++) {
        char c = s[i];
        char other = islower((unsigned char)c) ? (char)toupper((unsigned char)c) : (char)tolower((unsigned char)c);
        if (!memchr(s, other, n)) {
            char *left = longest_nice_substring(copy(s, i));
            char *right = longest_nice_substring(copy(s + i + 1, n - i - 1));
            free(s);
            if (strlen(right) > strlen(left)) {
                free(left);
                return right;
            }
            free(right);
            return left;
        }
    }
    return s;
}

int main(void) {
    int64_t seed = 1763;
    char *strings[1000];
    for (int j = 0; j < 1000; j++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t letters = 1 + seed / 65536 % 12;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t upper = seed / 65536 % 101;
        char *s = malloc(101);
        for (int i = 0; i < 100; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            int64_t base = seed / 65536 % 100 < upper ? 65 : 97;
            seed = (seed * 1103515245 + 12345) % 2147483648;
            s[i] = (char)(base + seed / 65536 % letters);
        }
        s[100] = 0;
        strings[j] = s;
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 500000; call++) {
        const char *s = strings[(check + call * 7919) % 1000];
        char *nice = longest_nice_substring(copy(s, strlen(s)));
        check = (check * 31 + (int64_t)strlen(nice)) % 1000000007;
        free(nice);
    }
    printf("500000 calls over 1000 strings: checksum %lld\n", (long long)check);
    for (int j = 0; j < 1000; j++) free(strings[j]);
    return 0;
}
