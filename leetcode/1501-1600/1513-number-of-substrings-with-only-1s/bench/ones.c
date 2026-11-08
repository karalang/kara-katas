// LeetCode #1513: Number of Substrings With Only 1s -- the bench: 20
// strings of 500000 bits built once, then each counted five times by the
// ★ arm.
#include <stdio.h>
#include <stdlib.h>

#define MOD 1000000007L

static long num_sub(const char *s) {
    long run = 0, total = 0;
    for (; *s; s++) {
        if (*s == '1') {
            run += 1;
            total += run;
        } else {
            run = 0;
        }
    }
    return total % MOD;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    long seed = 1513;
    char *strings[20];
    for (int k = 0; k < 20; k++) {
        strings[k] = malloc(500001);
        for (int i = 0; i < 500000; i++) strings[k][i] = next_random(&seed) % 20 < k ? '1' : '0';
        strings[k][500000] = 0;
    }
    long check = 0;
    for (int r = 0; r < 5; r++)
        for (int k = 0; k < 20; k++) check = (check * 31 + num_sub(strings[k]) + 1) % 1000000007;
    printf("100 counts over 20 strings of 500000 bits: checksum %ld\n", check);
    for (int k = 0; k < 20; k++) free(strings[k]);
    return 0;
}
