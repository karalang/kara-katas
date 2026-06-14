// LeetCode #415 bench — C bare-metal floor (mirror of add_strings.kara).
//
// Same two-pointer column add + digit-table render, but C renders each result
// into a stack buffer and never allocates a heap string per call — the
// no-allocation floor the Kāra/Rust/Go String builders are measured against.
// Sink is the running byte-sum of every rendered result (sum is commutative, so
// summing per-result == checksumming one giant concatenation).
#include <stdio.h>
#include <string.h>
#include <stdint.h>

static const char D[] = "0123456789";

// Decimal render of n into buf (not NUL-terminated); returns length.
static int digits_of(int64_t n, char *buf) {
    if (n == 0) { buf[0] = '0'; return 1; }
    char tmp[24];
    int t = 0;
    int64_t v = n;
    while (v > 0) { tmp[t++] = D[v % 10]; v /= 10; }
    for (int i = 0; i < t; i++) buf[i] = tmp[t - 1 - i];
    return t;
}

// Column add of decimal strings a[la] + b[lb] into out; returns length.
static int add_strings(const char *a, int la, const char *b, int lb, char *out) {
    int i = la - 1, j = lb - 1, carry = 0;
    char tmp[64];
    int t = 0;
    while (i >= 0 || j >= 0 || carry > 0) {
        int sum = carry;
        if (i >= 0) { sum += a[i] - '0'; i--; }
        if (j >= 0) { sum += b[j] - '0'; j--; }
        tmp[t++] = D[sum % 10];
        carry = sum / 10;
    }
    for (int k = 0; k < t; k++) out[k] = tmp[t - 1 - k];
    return t;
}

int main(void) {
    const int64_t total = 500000;
    const char *a = "31415926535897932384626433832795028841";
    const int la = (int)strlen(a);
    int64_t sum = 0;
    char bbuf[24], rbuf[64];
    for (int64_t k = 0; k < total; k++) {
        int64_t v = (k * 2654435761LL) & 0xffffffffLL;
        int lb = digits_of(v, bbuf);
        int lr = add_strings(a, la, bbuf, lb, rbuf);
        for (int i = 0; i < lr; i++) sum += (unsigned char)rbuf[i];
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
