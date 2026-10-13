// Benchmark for #504 in C: the ★ arm (the digits by repeated division);
// see ../convert_to_base7.kara. Each digit is formatted with snprintf
// and the answer is a fresh malloc'd string, freed after it is read.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *convert_to_base7(int64_t num) {
    char *out = malloc(16);
    if (num == 0) {
        strcpy(out, "0");
        return out;
    }
    int64_t n = num < 0 ? -num : num;
    int64_t digits[16];
    int count = 0;
    while (n > 0) {
        digits[count++] = n % 7;
        n /= 7;
    }
    size_t len = 0;
    if (num < 0) out[len++] = '-';
    for (int k = count - 1; k >= 0; k--) {
        char d[4];
        int w = snprintf(d, sizeof d, "%lld", (long long)digits[k]);
        memcpy(out + len, d, (size_t)w);
        len += (size_t)w;
    }
    out[len] = '\0';
    return out;
}

int main(void) {
    // 5,000,001 numbers across the whole range, -10^7 to 10^7 in steps
    // of 4. Each string is read back as a decimal number, which the base
    // 7 digits name uniquely, and folded into a checksum.
    const int64_t count = 5000001;
    int64_t digits = 0, checksum = 0;
    for (int64_t i = 0; i < count; i++) {
        int64_t num = -10000000 + 4 * i;
        char *s = convert_to_base7(num);
        digits += (int64_t)strlen(s);
        int64_t read = strtoll(s, NULL, 10);
        checksum = (checksum * 31 + read % 1000000007 + 1000000007) % 1000000007;
        free(s);
    }
    printf("%lld numbers: %lld characters, checksum %lld\n", (long long)count, (long long)digits,
           (long long)checksum);
    return 0;
}
