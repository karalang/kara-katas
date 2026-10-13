// Benchmark for #500: C mirror of the ★ arm (a row number for every
// letter); see keyboard_row.kara. Each word is lower-cased into a fresh
// buffer and each kept word copied into the output, as the Kāra arm
// does with `to_lowercase()` and `clone()`; the output array grows by
// doubling, as a Vec does when pushed to.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *s;
    int64_t len;
} Word;

static Word *find_words(const Word *words, int64_t n, int64_t *count) {
    static const char *rows[3] = {"qwertyuiop", "asdfghjkl", "zxcvbnm"};
    int64_t row_of[26] = {0};
    for (int r = 0; r < 3; r++) {
        for (const char *p = rows[r]; *p; p++) {
            row_of[*p - 'a'] = r;
        }
    }
    int64_t cap = 4, k = 0;
    Word *out = malloc(cap * sizeof(Word));
    for (int64_t i = 0; i < n; i++) {
        int64_t len = words[i].len;
        char *lower = malloc(len + 1);
        for (int64_t j = 0; j < len; j++) {
            char ch = words[i].s[j];
            lower[j] = (ch >= 'A' && ch <= 'Z') ? ch - 'A' + 'a' : ch;
        }
        int64_t first = -1;
        int one_row = 1;
        for (int64_t j = 0; j < len; j++) {
            int64_t r = row_of[lower[j] - 'a'];
            if (first < 0) {
                first = r;
            } else if (r != first) {
                one_row = 0;
                break;
            }
        }
        free(lower);
        if (one_row) {
            if (k == cap) {
                cap *= 2;
                out = realloc(out, cap * sizeof(Word));
            }
            out[k].s = malloc(len + 1);
            memcpy(out[k].s, words[i].s, len + 1);
            out[k].len = len;
            k++;
        }
    }
    *count = k;
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    // 20,000 lists of 20 words of 1 to 100 letters, each word from one
    // row (2 in 3) or the whole alphabet, a letter upper case with odds
    // 1 in 4, built once. Then each list is solved once.
    static const char *pools[4] = {"qwertyuiop", "asdfghjkl", "zxcvbnm", "abcdefghijklmnopqrstuvwxyz"};
    int64_t lists = 20000;
    int64_t seed = 500;
    Word *all = malloc(lists * 20 * sizeof(Word));
    for (int64_t l = 0; l < lists; l++) {
        for (int w = 0; w < 20; w++) {
            int64_t pool = next_random(&seed) % 3 == 0 ? 3 : next_random(&seed) % 3;
            int64_t length = 1 + next_random(&seed) % 100;
            int64_t plen = (int64_t)strlen(pools[pool]);
            char *s = malloc(length + 1);
            for (int64_t i = 0; i < length; i++) {
                char ch = pools[pool][next_random(&seed) % plen];
                s[i] = next_random(&seed) % 4 == 0 ? ch - 'a' + 'A' : ch;
            }
            s[length] = 0;
            all[l * 20 + w].s = s;
            all[l * 20 + w].len = length;
        }
    }
    int64_t kept = 0, letters = 0, checksum = 0;
    for (int64_t l = 0; l < lists; l++) {
        int64_t count;
        Word *got = find_words(all + l * 20, 20, &count);
        for (int64_t i = 0; i < count; i++) {
            kept++;
            letters += got[i].len;
            checksum = (checksum * 31 + got[i].len + got[i].s[0]) % 1000000007;
            free(got[i].s);
        }
        free(got);
    }
    printf("%lld lists of 20 words: %lld words kept, %lld letters, checksum %lld\n",
           (long long)lists, (long long)kept, (long long)letters, (long long)checksum);
    return 0;
}
