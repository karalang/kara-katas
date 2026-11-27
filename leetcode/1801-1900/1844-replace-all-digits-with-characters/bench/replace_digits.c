// LeetCode #1844: Replace All Digits with Characters -- the bench in C: the ★ arm over
// 500000 calls on 40 strings of 100 places, built once, each call's string
// drawn from the checksum so far and one byte of its output, at a place
// drawn the same way, folded in. Each call builds its own output string.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *replace_digits(const char *s) {
    size_t n = strlen(s);
    char *out = malloc(n + 1);
    for (size_t i = 0; i < n; i++) {
        if (i % 2 == 0) out[i] = s[i];
        else out[i] = (char)(s[i - 1] + s[i] - '0');
    }
    out[n] = 0;
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1844;
    char *cases[40];
    for (int c = 0; c < 40; c++) {
        cases[c] = malloc(101);
        int64_t letter = 0;
        for (int i = 0; i < 100; i++) {
            if (i % 2 == 0) {
                letter = next_random(&seed) % 26;
                cases[c][i] = (char)('a' + letter);
            } else {
                int64_t most = 25 - letter < 9 ? 25 - letter : 9;
                cases[c][i] = (char)('0' + next_random(&seed) % (most + 1));
            }
        }
        cases[c][100] = 0;
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 500000; call++) {
        char *out = replace_digits(cases[(check + call) % 40]);
        check = (check * 31 + (unsigned char)out[(check / 40 + call) % 100]) % 1000000007;
        free(out);
    }
    printf("500000 calls: checksum %lld\n", (long long)check);
    return 0;
}
