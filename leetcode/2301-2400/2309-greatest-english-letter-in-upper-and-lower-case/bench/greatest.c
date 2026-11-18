// LeetCode #2309: Greatest English Letter in Upper and Lower Case -- the
// bench, the ★ arm in C. A mask of the lowercase letters and one of the
// uppercase; the highest bit of their & is the answer, 0 for none.
#include <stdint.h>
#include <stdio.h>

enum { STRINGS = 1000, LEN = 1000 };

static int greatest_letter(const char *s, int n) {
    int64_t lower = 0, upper = 0;
    for (int i = 0; i < n; i++) {
        unsigned char b = (unsigned char)s[i];
        if (b >= 'a')
            lower |= (int64_t)1 << (b - 'a');
        else
            upper |= (int64_t)1 << (b - 'A');
    }
    int64_t both = lower & upper;
    for (int i = 25; i >= 0; i--)
        if ((both >> i) & 1) return 'A' + i;
    return 0;
}

static int64_t seed = 2309;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const char *letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    static char strings[STRINGS][LEN];
    for (int a = 0; a < STRINGS; a++) {
        int64_t pool = next_random() % 30 + 1;
        char from[30];
        for (int64_t i = 0; i < pool; i++) from[i] = letters[next_random() % 52];
        for (int i = 0; i < LEN; i++) strings[a][i] = from[next_random() % pool];
    }
    int64_t check = 0;
    for (int p = 0; p < 100; p++)
        for (int a = 0; a < STRINGS; a++) check = (check * 31 + greatest_letter(strings[a], LEN)) % 1000000007;
    printf("100 passes over 1000 strings of 1000 letters: checksum %lld\n", (long long)check);
    return 0;
}
