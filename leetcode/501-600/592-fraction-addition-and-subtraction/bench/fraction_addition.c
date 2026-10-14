// Benchmark for #592: C mirror of the ★ arm (a running sum, reduced as it
// goes); see fraction_addition.kara. The expression is read in place, its
// bytes being its characters, and the answer written into a buffer the
// caller gives.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t gcd(int64_t a, int64_t b) {
    if (b == 0)
        return a < 0 ? -a : a;
    return gcd(b, a % b);
}

static int64_t digits(const char *e, int64_t n, int64_t i, int64_t *end) {
    int64_t value = 0, j = i;
    while (j < n && e[j] >= '0' && e[j] <= '9') {
        value = value * 10 + (e[j] - '0');
        j++;
    }
    *end = j;
    return value;
}

static void fraction_addition(const char *e, int64_t n, char *out) {
    int64_t num = 0, den = 1, i = 0;
    while (i < n) {
        int64_t sign = 1;
        if (e[i] == '-' || e[i] == '+') {
            if (e[i] == '-')
                sign = -1;
            i++;
        }
        int64_t after_a, after_b;
        int64_t a = digits(e, n, i, &after_a);
        int64_t b = digits(e, n, after_a + 1, &after_b);
        i = after_b;
        int64_t common = den / gcd(den, b) * b;
        num = num * (common / den) + sign * a * (common / b);
        den = common;
        int64_t g = gcd(num, den);
        num /= g;
        den /= g;
    }
    snprintf(out, 48, "%lld/%lld", (long long)num, (long long)den);
}

// ---- benchmark --------------------------------------------------------------

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int coprime(int64_t a, int64_t b) {
    while (b != 0) {
        int64_t t = a % b;
        a = b;
        b = t;
    }
    return a == 1;
}

static int64_t expression(int64_t count, int64_t *seed, char *out) {
    int64_t len = 0;
    for (int64_t k = 0; k < count; k++) {
        int64_t a = 1 + step(seed) % 10;
        int64_t b = 1 + step(seed) % 10;
        while (!coprime(a, b)) {
            a = 1 + step(seed) % 10;
            b = 1 + step(seed) % 10;
        }
        if (step(seed) % 2 == 0)
            out[len++] = '-';
        else if (k > 0)
            out[len++] = '+';
        len += sprintf(out + len, "%lld/%lld", (long long)a, (long long)b);
    }
    out[len] = '\0';
    return len;
}

int main(void) {
    enum { COUNT = 1000, ROUNDS = 1000 };
    int64_t seed = 592;
    static char expressions[COUNT][64];
    static int64_t lens[COUNT];
    for (int k = 0; k < COUNT; k++)
        lens[k] = expression(10, &seed, expressions[k]);
    int64_t negative = 0, checksum = 0;
    char got[48];
    for (int round = 0; round < ROUNDS; round++)
        for (int g = 0; g < COUNT; g++) {
            int c = (round * 7 + g) % COUNT;
            fraction_addition(expressions[c], lens[c], got);
            if (got[0] == '-')
                negative++;
            for (char *p = got; *p; p++)
                checksum = (checksum * 31 + *p) % 1000000007;
        }
    printf("%d expressions, %d rounds: %lld negative, checksum %lld\n", COUNT, ROUNDS, (long long)negative,
           (long long)checksum);
    return 0;
}
