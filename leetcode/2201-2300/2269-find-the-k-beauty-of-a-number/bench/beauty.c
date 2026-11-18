// LeetCode #2269: Find the K-Beauty of a Number -- the bench, the ★ arm.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t divisor_substrings(int64_t num, int64_t k) {
    char s[24], part_s[24];
    int64_t n = snprintf(s, sizeof s, "%lld", (long long)num);
    int64_t beauty = 0;
    for (int64_t i = 0; i <= n - k; i++) {
        memcpy(part_s, s + i, k);
        part_s[k] = 0;
        int64_t part = strtoll(part_s, NULL, 10);
        if (part != 0 && num % part == 0) beauty++;
    }
    return beauty;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2269;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0;
    for (int64_t t = 0; t < 200000; t++) {
        int64_t hi = next_random();
        int64_t num = (hi * 32768 + next_random()) % 1000000000 + 1;
        char s[24];
        int64_t len = snprintf(s, sizeof s, "%lld", (long long)num);
        int64_t k = t % 9 + 1 < len ? t % 9 + 1 : len;
        check = (check * 31 + divisor_substrings(num, k)) % 1000000007;
    }
    printf("200000 numbers: checksum %lld\n", (long long)check);
    return 0;
}
