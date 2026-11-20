// LeetCode #1271 bench, in C: the ★ arm (the decimal text parsed, its
// hexadecimal digits spelled from the lowest, 0 as O, 1 as I, 10 to 15 as A
// to F, any other an error) on 100,000 numbers up to 10^12 drawn once, half
// spelled in the eight letters, 150 rounds; every answer folded into a
// checksum.
// The answer is written into a caller's buffer.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void to_hexspeak(const char *num, char *out) {
    int64_t n = strtoll(num, NULL, 10);
    char letters[16];
    int len = 0;
    while (n > 0) {
        int64_t d = n % 16;
        if (d == 0) letters[len++] = 'O';
        else if (d == 1) letters[len++] = 'I';
        else if (d >= 10) letters[len++] = 'A' + (d - 10);
        else {
            strcpy(out, "ERROR");
            return;
        }
        n /= 16;
    }
    for (int i = 0; i < len; i++) out[i] = letters[len - 1 - i];
    out[len] = 0;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1271;
    static const int64_t letters[8] = {0, 1, 10, 11, 12, 13, 14, 15};
    static char nums[100000][16];
    for (int i = 0; i < 100000; i++) {
        int64_t n;
        if (i % 2 == 0) {
            int64_t a = next_random(&seed);
            int64_t b = next_random(&seed);
            n = (a * 32768 + b) % 1000000000000LL + 1;
        } else {
            n = 1;
            int64_t k = next_random(&seed) % 9;
            for (int64_t j = 0; j < k; j++) n = n * 16 + letters[next_random(&seed) % 8];
        }
        snprintf(nums[i], sizeof nums[i], "%lld", (long long)n);
    }
    char out[32];
    int64_t check = 0;
    for (int64_t round = 0; round < 150; round++)
        for (int i = 0; i < 100000; i++) {
            to_hexspeak(nums[i], out);
            int64_t len = strlen(out);
            check = (check * 131 + len + round) % 1000000007;
            for (int j = 0; j < len; j++) check = (check * 131 + (unsigned char)out[j]) % 1000000007;
        }
    printf("150 rounds of 100000 numbers: checksum %lld\n", (long long)check);
    return 0;
}
