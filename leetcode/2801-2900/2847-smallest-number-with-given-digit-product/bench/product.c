// LeetCode #2847: Smallest Number With Given Digit Product -- the
// bench, mirrored from product.kara: the largest digit that divides
// what is left, 9 down to 2, and the digits smallest first, into a
// fresh buffer each time.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *smallest_number(int64_t n) {
    char *out = malloc(72);
    if (n == 1) {
        strcpy(out, "1");
        return out;
    }
    char digits[72];
    int len = 0;
    int64_t rest = n;
    for (int d = 9; d >= 2; d--) {
        while (rest % d == 0) {
            digits[len++] = (char)('0' + d);
            rest /= d;
        }
    }
    if (rest != 1) {
        strcpy(out, "-1");
        return out;
    }
    for (int i = 0; i < len; i++) out[i] = digits[len - 1 - i];
    out[len] = 0;
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const long count = 100000, rounds = 20;
    int64_t seed = 2847;
    int64_t *numbers = malloc(count * sizeof(int64_t));
    const int64_t primes[4] = {2, 3, 5, 7};
    for (long c = 0; c < count; c++) {
        int64_t n = 1;
        int64_t factors = next_random(&seed) % 41;
        for (int64_t i = 0; i < factors; i++) {
            int64_t p = primes[next_random(&seed) % 4];
            if (n <= 1000000000000000000LL / p) n *= p;
        }
        if (next_random(&seed) % 10 == 0 && n <= 1000000000000000000LL / 11) n *= 11;
        numbers[c] = n;
    }
    int64_t digits = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (long c = 0; c < count; c++) {
            char *s = smallest_number(numbers[c]);
            size_t len = strlen(s);
            digits += (int64_t)len;
            for (size_t i = 0; i < len; i++) check = (check * 31 + (unsigned char)s[i] + r) % 1000000007;
            free(s);
        }
    }
    printf("%ld numbers, %ld rounds: %lld digits, checksum %lld\n", count, rounds, (long long)digits, (long long)check);
    free(numbers);
    return 0;
}
