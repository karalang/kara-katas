// LeetCode #2276: Percentage of Letter in String -- the bench, the ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t percentage_letter(const char *s, char letter) {
    int64_t count = 0;
    int64_t n = (int64_t)strlen(s);
    for (int64_t i = 0; i < n; i++) {
        if (s[i] == letter) count++;
    }
    return count * 100 / n;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2276;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0;
    for (int t = 0; t < 100000; t++) {
        char *s = malloc(101);
        for (int i = 0; i < 100; i++) s[i] = (char)('a' + next_random() % 4);
        s[100] = '\0';
        char letter = (char)('a' + next_random() % 4);
        check = (check * 31 + percentage_letter(s, letter)) % 1000000007;
        free(s);
    }
    printf("100000 strings of 100: checksum %lld\n", (long long)check);
    return 0;
}
