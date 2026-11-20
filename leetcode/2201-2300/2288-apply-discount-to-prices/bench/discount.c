// LeetCode #2288: Apply Discount to Prices -- the bench, the ★ arm in C.
// Split on spaces; a `$` and then only digits is a price, discounted in
// whole cents and written back with two decimals.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int is_price(const char *w, size_t n) {
    if (n < 2 || w[0] != '$') return 0;
    for (size_t i = 1; i < n; i++)
        if (w[i] < '0' || w[i] > '9') return 0;
    return 1;
}

// writes the answer into `out`, returns its length
static size_t discount_prices(const char *s, size_t len, int64_t discount, char *out) {
    size_t o = 0, start = 0;
    for (size_t i = 0; i <= len; i++) {
        if (i < len && s[i] != ' ') continue;
        if (start > 0) out[o++] = ' ';
        size_t n = i - start;
        if (is_price(s + start, n)) {
            int64_t price = 0;
            for (size_t j = start + 1; j < i; j++) price = price * 10 + (s[j] - '0');
            int64_t cents = price * (100 - discount);
            o += (size_t)sprintf(out + o, "$%lld.%02lld", (long long)(cents / 100), (long long)(cents % 100));
        } else {
            memcpy(out + o, s + start, n);
            o += n;
        }
        start = i + 1;
    }
    out[o] = 0;
    return o;
}

static int64_t seed = 2288;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static size_t word(char *w) {
    int64_t kind = next_random() % 4;
    int64_t len = next_random() % 8 + 1;
    size_t n = 0;
    if (kind < 2) w[n++] = '$';
    for (int64_t i = 0; i < len; i++) {
        int64_t r = next_random();
        w[n++] = (kind == 0 || kind == 3) ? (char)('0' + r % 10) : (char)('a' + r % 26);
    }
    return n;
}

int main(void) {
    enum { N = 4000 };
    static char text[N][128];
    static size_t lens[N];
    for (int k = 0; k < N; k++) {
        size_t n = 0;
        for (int i = 0; i < 12; i++) {
            if (i > 0) text[k][n++] = ' ';
            n += word(text[k] + n);
        }
        text[k][n] = 0;
        lens[k] = n;
    }
    static char out[512];
    int64_t check = 0;
    for (int64_t pass = 0; pass < 50; pass++) {
        for (int k = 0; k < N; k++) {
            size_t n = discount_prices(text[k], lens[k], pass * 2, out);
            check = (check * 31 + (int64_t)n + (unsigned char)out[n - 2]) % 1000000007;
        }
    }
    printf("50 passes over 4000 sentences: checksum %lld\n", (long long)check);
    return 0;
}
