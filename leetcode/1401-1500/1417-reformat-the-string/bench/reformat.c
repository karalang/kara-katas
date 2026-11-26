// LeetCode #1417 bench, C: the letters and the digits apart, each in its
// order, woven together from the larger group, workload and checksum as
// reformat.kara. The two groups and the answer are heap buffers, as the
// Kāra `Vec`s and `String` are.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static char *reformat(const char *s, size_t n, size_t *len) {
    char *letters = malloc(n), *digits = malloc(n);
    size_t nl = 0, nd = 0;
    for (size_t i = 0; i < n; i++) {
        if (s[i] >= 'a' && s[i] <= 'z') {
            letters[nl++] = s[i];
        } else if (s[i] >= '0' && s[i] <= '9') {
            digits[nd++] = s[i];
        }
    }
    char *out = malloc(n + 1);
    *len = 0;
    if ((nl > nd ? nl - nd : nd - nl) <= 1) {
        char *first = nd > nl ? digits : letters, *second = nd > nl ? letters : digits;
        size_t nf = nd > nl ? nd : nl, ns = nd > nl ? nl : nd;
        for (size_t i = 0; i < nf; i++) {
            out[(*len)++] = first[i];
            if (i < ns) {
                out[(*len)++] = second[i];
            }
        }
    }
    free(letters);
    free(digits);
    return out;
}

int main(void) {
    int64_t seed = 1417, check = 0;
    const char letters[6] = {'a', 'b', 'c', 'x', 'y', 'z'};
    char *pool = malloc(200000);
    for (int i = 0; i < 100000; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t r = seed / 65536;
        char letter = letters[r % 6], digit = (char)('0' + r / 6 % 10);
        if (r / 60 % 2 == 0) {
            pool[2 * i] = letter;
            pool[2 * i + 1] = digit;
        } else {
            pool[2 * i] = digit;
            pool[2 * i + 1] = letter;
        }
    }
    for (int w = 0; w < 20000; w++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        size_t start = (size_t)(2 * (seed / 65536 % 99750));
        size_t len;
        char *out = reformat(pool + start, 500, &len);
        int64_t sum = 0;
        for (size_t k = 0; k < len; k++) {
            sum = (sum * 31 + (unsigned char)out[k]) % 1000000007;
        }
        free(out);
        check = (check * 131 + sum) % 1000000007;
    }
    printf("20000 windows of 500 characters: checksum %lld\n", (long long)check);
    free(pool);
    return 0;
}
