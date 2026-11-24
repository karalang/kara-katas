// LeetCode #1328 bench, C mirror of the Kāra bench: the ★ arm (the letters
// into an array of code points, the first half searched for a letter that
// is not an a, the answer written back into a fresh string) on 20
// palindromes of 10^5 letters built once, in four kinds: all a; a until the
// last tenth of the half, then random letters; a with a rare b; and random
// letters. Then 800 passes, each setting one mirrored pair of every
// palindrome from the checksum so far, answering it and folding two of the
// answer's letters plus the pass into the checksum. Each call copies its
// input as the Kāra bench's `String.from_utf8(..clone())` does, and takes
// a fresh `malloc` for the letters and the answer, as the Kāra arm takes a
// fresh `Vec[char]` and `String`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *break_palindrome(const char *palindrome, int64_t n) {
    uint32_t *chars = malloc((size_t)n * sizeof(uint32_t));
    for (int64_t i = 0; i < n; i++) chars[i] = (unsigned char)palindrome[i];
    char *out;
    if (n == 1) {
        free(chars);
        out = malloc(1);
        out[0] = 0;
        return out;
    }
    int64_t i = 0;
    for (; i < n / 2; i++) {
        if (chars[i] != 'a') {
            chars[i] = 'a';
            break;
        }
    }
    if (i == n / 2) chars[n - 1] = 'b';
    out = malloc((size_t)n + 1);
    for (int64_t k = 0; k < n; k++) out[k] = (char)chars[k];
    out[n] = 0;
    free(chars);
    return out;
}

static int64_t seed = 1328;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 100000;
    const char *letters = "abcdefghijklmnopqrstuvwxyz";
    static char texts[20][100000];
    for (int t = 0; t < 20; t++) {
        int kind = t % 4;
        memset(texts[t], 'a', (size_t)n);
        for (int64_t i = 0; i < n / 2; i++) {
            char c;
            if (kind == 0) c = 'a';
            else if (kind == 1) c = i < n / 2 - n / 20 ? 'a' : letters[next_random() % 26];
            else if (kind == 2) c = next_random() % 2000 == 0 ? 'b' : 'a';
            else c = letters[next_random() % 26];
            texts[t][i] = c;
            texts[t][n - 1 - i] = c;
        }
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 800; pass++) {
        for (int t = 0; t < 20; t++) {
            int64_t j = check % (n / 2);
            char c = (check / 7) % 4 == 0 ? 'b' : 'a';
            texts[t][j] = c;
            texts[t][n - 1 - j] = c;
            char *copy = malloc((size_t)n);
            memcpy(copy, texts[t], (size_t)n);
            char *got = break_palindrome(copy, n);
            check = (check * 31 + (unsigned char)got[j] + (unsigned char)got[n - 1] + pass) % 1000000007;
            free(got);
            free(copy);
        }
    }
    printf("800 passes over 20 palindromes of 10^5: checksum %lld\n", (long long)check);
    return 0;
}
