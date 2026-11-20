// LeetCode #1663 bench: the ★ arm, from the back.
//
// 400 problems with n = 10^5, LeetCode's largest, and k drawn from n to
// 26n, all drawn first; then each string is built and every letter of it
// folded into a checksum.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// a fresh string of n letters, as the other languages return one
static char *get_smallest_string(int32_t n, int32_t k) {
    char *letters = malloc((size_t)n + 1);
    memset(letters, 'a', (size_t)n);
    letters[n] = 0;
    int64_t left = (int64_t)k - n;
    int64_t i = n - 1;
    while (left > 0) {
        int64_t more = left < 25 ? left : 25;
        letters[i] += (char)more;
        left -= more;
        i--;
    }
    return letters;
}

static int64_t seed;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    enum { COUNT = 400 };
    const int64_t n = 100000;
    seed = 1663;
    int32_t ks[COUNT];
    for (int c = 0; c < COUNT; c++) {
        int64_t r = next_random() * 32768;
        r += next_random();
        ks[c] = (int32_t)(n + r % (25 * n + 1));
    }
    int64_t zs = 0, check = 0;
    for (int c = 0; c < COUNT; c++) {
        char *s = get_smallest_string((int32_t)n, ks[c]);
        for (int64_t i = 0; i < n; i++) {
            unsigned char b = (unsigned char)s[i];
            if (b == 'z') zs++;
            check = (check * 31 + b) % 1000000007;
        }
        free(s);
    }
    printf("%d problems with n = %lld: %lld z's, checksum %lld\n", COUNT, (long long)n, (long long)zs,
           (long long)check);
    return 0;
}
