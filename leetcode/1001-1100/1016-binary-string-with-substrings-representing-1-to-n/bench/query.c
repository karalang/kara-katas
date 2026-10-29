// LeetCode #1016: Binary String With Substrings Representing 1 To N --
// bench
// Mirrors query.kara; see ../README.md § Benchmarks.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

// x's binary form, most significant bit first
static void binary_form(int64_t x, char *out) {
    char rev[65];
    int k = 0;
    while (x > 0) {
        rev[k++] = (char)('0' + (x & 1));
        x >>= 1;
    }
    for (int i = 0; i < k; i++) {
        out[i] = rev[k - 1 - i];
    }
    out[k] = '\0';
}

static bool query_string(const char *s, int64_t len, int64_t n) {
    if (n - n / 2 > 2 * len) {
        return false;
    }
    char form[65];
    for (int64_t x = n; x > n / 2; x--) {
        binary_form(x, form);
        if (strstr(s, form) == NULL) {
            return false;
        }
    }
    return true;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t strings = 200;
    int64_t len = 1000;
    int64_t most = 400;
    int64_t seed = 1016;
    int64_t holds = 0;
    int64_t check = 0;
    char s[1001];
    for (int64_t t = 0; t < strings; t++) {
        for (int64_t i = 0; i < len; i++) {
            s[i] = next_random(&seed) % 2 == 1 ? '1' : '0';
        }
        s[len] = '\0';
        for (int64_t n = 1; n < most + 1; n++) {
            bool answer = query_string(s, len, n);
            if (answer) {
                holds++;
            }
            check = (check * 2 + (answer ? 1 : 0)) % 1000000007;
        }
    }
    printf("%lld strings of %lld bits, n = 1..%lld: %lld hold, checksum %lld\n", (long long)strings,
           (long long)len, (long long)most, (long long)holds, (long long)check);
    return 0;
}
