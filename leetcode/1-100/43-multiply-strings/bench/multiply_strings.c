// LeetCode #43 bench — C bare-metal floor (mirror of multiply_strings.kara).
//
// Same digit-grid multiply + digit-table render, but C renders each result into
// a stack buffer and never allocates a heap string per call — the no-allocation
// floor the Kāra/Rust/Go String builders are measured against. Sink is the
// running byte-sum of every rendered result (sum is commutative, so summing
// per-result == checksumming one giant concatenation).
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

// Digit-grid multiply of decimal strings a[la] * b[lb] into out; returns length.
static int multiply(const char *a, int la, const char *b, int lb, char *out) {
    int64_t res[128];
    int mn = la + lb;
    for (int i = 0; i < mn; i++) res[i] = 0;
    for (int i = la - 1; i >= 0; i--) {
        int64_t d1 = a[i] - '0';
        for (int j = lb - 1; j >= 0; j--) {
            int64_t d2 = b[j] - '0';
            int lo = i + j + 1, hi = i + j;
            int64_t sum = d1 * d2 + res[lo];
            res[lo] = sum % 10;
            res[hi] += sum / 10;
        }
    }
    int k = 0;
    while (k < mn && res[k] == 0) k++;
    int t = 0;
    while (k < mn) out[t++] = D[res[k++]];
    if (t == 0) { out[0] = '0'; return 1; }
    return t;
}

int main(void) {
    const int64_t total = 300000;
    const char *a = "31415926535897932384626433832795028841";
    const int la = (int)strlen(a);
    int64_t sum = 0;
    char bbuf[24], rbuf[128];
    for (int64_t k = 0; k < total; k++) {
        int64_t v = (k * 2654435761LL) & 0xffffffffLL;
        int lb = digits_of(v, bbuf);
        int lr = multiply(a, la, bbuf, lb, rbuf);
        for (int i = 0; i < lr; i++) sum += (unsigned char)rbuf[i];
    }
    printf("%lld\n", (long long)sum);
    return 0;
}
