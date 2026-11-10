// LeetCode #2075: Decode the Slanted Ciphertext -- C mirror of the ★ arm's
// benchmark (slanted.kara): 40 grids of 10^6 characters in 1 to 1000 rows,
// built once and decoded into a growing buffer.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static size_t decode_ciphertext(const char *text, int64_t n, int64_t rows, char *plain) {
    int64_t cols = n / rows;
    size_t len = 0;
    for (int64_t c = 0; c < cols; c++)
        for (int64_t r = 0; r < rows && c + r < cols; r++) plain[len++] = text[r * cols + c + r];
    while (len > 0 && plain[len - 1] == ' ') len--;
    return len;
}

int main(void) {
    const char *letters = "abcdefghijklmnopqrstuvwxyz      ";
    int64_t seed = 2075;
    char *texts[40];
    int64_t lens[40], rowss[40];
    int64_t rowlist[5] = {1, 2, 10, 100, 1000};
    for (int g = 0; g < 40; g++) {
        int64_t rows = rowlist[g % 5], n = 1000000 / rows * rows;
        char *t = malloc(n);
        for (int64_t i = 0; i < n; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            t[i] = letters[(seed / 65536) % 32];
        }
        texts[g] = t; lens[g] = n; rowss[g] = rows;
    }
    char *plain = malloc(1000000);
    int64_t total = 0, check = 0;
    for (int g = 0; g < 40; g++) {
        size_t len = decode_ciphertext(texts[g], lens[g], rowss[g], plain);
        total += len;
        for (size_t i = 0; i < len; i++) check = (check * 31 + (unsigned char)plain[i]) % 1000000007;
    }
    printf("40 grids: %lld characters, checksum %lld\n", (long long)total, (long long)check);
    for (int g = 0; g < 40; g++) free(texts[g]);
    free(plain);
    return 0;
}
