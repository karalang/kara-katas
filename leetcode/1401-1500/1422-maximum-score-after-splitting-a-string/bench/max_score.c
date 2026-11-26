#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int32_t max_score(const char *s, int64_t n) {
    // the digits copied out, as the Kāra and Rust programs collect them
    uint8_t *digits = malloc(n);
    memcpy(digits, s, n);
    int32_t ones = 0;
    for (int64_t i = 0; i < n; i++) ones += digits[i] == '1';
    int32_t lead = 0, best = INT32_MIN;
    for (int64_t i = 0; i + 1 < n; i++) {
        lead += digits[i] == '0' ? 1 : -1;
        if (lead > best) best = lead;
    }
    free(digits);
    return ones + best;
}

int main(void) {
    int64_t seed = 1422;
    char *pool = malloc(1000000);
    for (int i = 0; i < 1000000; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        pool[i] = seed / 65536 % 2 == 0 ? '0' : '1';
    }
    int64_t check = 0;
    for (int w = 0; w < 1000000; w++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t start = seed / 65536 % 999501;
        check = (check * 131 + max_score(pool + start, 500)) % 1000000007;
    }
    printf("10^6 windows of 500 digits: checksum %lld\n", (long long)check);
    return 0;
}
