// LeetCode 800 — Similar RGB Color: the bench, in C. Mirrors
// similar_rgb.kara: each part rounded to the nearest doubled digit, the
// answer in a fresh allocation.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static const char DIGITS[] = "0123456789abcdef";

static int64_t digit(unsigned char c) {
    return (c >= 48 && c <= 57) ? c - 48 : c - 97 + 10;
}

static char *similar_rgb(const char *color) {
    char *out = malloc(8);
    out[0] = '#';
    for (int p = 0; p < 3; p++) {
        int64_t part = digit(color[1 + 2 * p]) * 16 + digit(color[2 + 2 * p]);
        char d = DIGITS[(part + 8) / 17];
        out[1 + 2 * p] = d;
        out[2 + 2 * p] = d;
    }
    out[7] = 0;
    return out;
}

static int64_t seed = 800;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char colors[4096][8];
    for (int i = 0; i < 4096; i++) {
        colors[i][0] = '#';
        for (int j = 1; j <= 6; j++) colors[i][j] = DIGITS[next_random() % 16];
        colors[i][7] = 0;
    }
    const int64_t rounds = 40960000;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        char *got = similar_rgb(colors[r % 4096]);
        check = (check * 31 + (int64_t)got[1] * 65536 + (int64_t)got[3] * 256 + got[5]) % 1000000007;
        free(got);
    }
    printf("%lld colours: checksum %lld\n", (long long)rounds, (long long)check);
    return 0;
}
