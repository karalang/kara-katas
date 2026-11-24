// LeetCode #1316 bench, C mirror of the Kāra bench: the ★ arm (a table of
// how far every two suffixes agree, each echo counted at the first place it
// starts) on 4 strings of 2000 letters built once; then 5 passes, each
// setting one letter of every string from the checksum so far, answering it
// and folding the count plus the pass into the checksum. Each call takes a
// fresh table, a `calloc`, as the Kāra arm takes a fresh `Vec`.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t distinct_echo_substrings(const char *s, int64_t n) {
    int64_t w = n + 1;
    int64_t *agree = calloc((size_t)(w * w), sizeof(int64_t));
    for (int64_t i = n - 1; i >= 0; i--)
        for (int64_t j = n - 1; j > i; j--)
            if (s[i] == s[j]) agree[i * w + j] = agree[(i + 1) * w + j + 1] + 1;
    int64_t *earlier = calloc((size_t)(n > 0 ? n : 1), sizeof(int64_t));
    for (int64_t i = 0; i < n; i++)
        for (int64_t j = i + 1; j < n; j++)
            if (agree[i * w + j] > earlier[j]) earlier[j] = agree[i * w + j];
    int64_t count = 0;
    for (int64_t i = 0; i < n; i++)
        for (int64_t h = 1; h <= (n - i) / 2; h++)
            if (agree[i * w + i + h] >= h && 2 * h > earlier[i]) count++;
    free(earlier);
    free(agree);
    return (int32_t)count;
}

static int64_t seed = 1316;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 2000;
    const char *letters = "abcdefghijklmnopqrstuvwxyz";
    char strings[4][2001];
    for (int t = 0; t < 4; t++) {
        if (t == 3) {
            char block[3];
            for (int b = 0; b < 3; b++) block[b] = letters[next_random() % 26];
            for (int64_t i = 0; i < n; i++) strings[t][i] = block[i % 3];
        } else {
            int64_t k = t == 0 ? 2 : t == 1 ? 3 : 26;
            for (int64_t i = 0; i < n; i++) strings[t][i] = letters[next_random() % k];
        }
        strings[t][n] = 0;
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 5; pass++) {
        for (int t = 0; t < 4; t++) {
            strings[t][check % n] = letters[(check / 7) % 26];
            int64_t count = distinct_echo_substrings(strings[t], n);
            check = (check * 31 + count + pass) % 1000000007;
        }
    }
    printf("5 passes over 4 strings of 2000: checksum %lld\n", (long long)check);
    return 0;
}
