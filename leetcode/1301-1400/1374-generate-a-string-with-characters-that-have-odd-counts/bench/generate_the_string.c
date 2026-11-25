// LeetCode #1374 bench -- C: the ★ arm: n a's when n is odd, and n - 1
// a's and a b when it is even, in a fresh heap buffer.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *generate_the_string(int n) {
    char *s = malloc((size_t)n + 1);
    memset(s, 'a', (size_t)n);
    if (n % 2 == 0) s[n - 1] = 'b';
    s[n] = '\0';
    return s;
}

int main(void) {
    // 10^7 rounds, each making the string for an n from 1 to 500, the
    // constraints' range, drawn from the checksum so far, and reading its
    // length and one letter at a place drawn the same way
    int64_t check = 0;
    for (int64_t r = 0; r < 10000000; r++) {
        int n = (int)(1 + check % 500);
        char *s = generate_the_string(n);
        int64_t len = n;  // the buffer holds n letters
        int64_t b = (unsigned char)s[(check / 500) % len];
        free(s);
        check = (check * 31 + len + b + r) % 1000000007;
    }
    printf("10000000 rounds: checksum %lld\n", (long long)check);
    return 0;
}
