// LeetCode #1758: Minimum Changes To Make Alternating Binary String -- the
// bench in C, mirroring min_operations.kara: one pass counting the
// characters that differ from "0101...".
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int min_operations(const char *s, int64_t n) {
    int64_t differ = 0;
    for (int64_t i = 0; i < n; i++) {
        if ((int64_t)(s[i] - '0') != i % 2) differ++;
    }
    return (int)(differ < n - differ ? differ : n - differ);
}

int main(void) {
    int64_t seed = 1758;
    char *strings[2000];
    int64_t lengths[2000];
    for (int j = 0; j < 2000; j++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t n = 1 + seed / 65536 % 20000;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t chance = seed / 65536 % 101;
        char *s = malloc(n + 1);
        for (int64_t i = 0; i < n; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            s[i] = seed / 65536 % 100 < chance ? '1' : '0';
        }
        s[n] = 0;
        strings[j] = s;
        lengths[j] = n;
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 30000; call++) {
        int64_t at = (check + call * 7919) % 2000;
        check = (check * 31 + min_operations(strings[at], lengths[at])) % 1000000007;
    }
    printf("30000 calls over 2000 strings: checksum %lld\n", (long long)check);
    for (int j = 0; j < 2000; j++) free(strings[j]);
    return 0;
}
