// LeetCode #2108: Find First Palindromic String in the Array -- the
// benchmark, the same algorithm as palindrome.kara: each word's bytes read
// from both ends towards the middle.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define WORDS 100
#define LEN 100

static int is_palindrome(const char *w, int64_t n) {
    int64_t i = 0, j = n - 1;
    while (i < j) {
        if (w[i] != w[j]) return 0;
        i++;
        j--;
    }
    return 1;
}

// Returns the index of the first palindrome, or -1 for none; the caller
// copies it out as the other languages' `clone` does.
static int64_t first_palindrome(char words[][LEN + 1], char *out) {
    for (int64_t k = 0; k < WORDS; k++) {
        int64_t n = (int64_t)strlen(words[k]);
        if (is_palindrome(words[k], n)) {
            memcpy(out, words[k], (size_t)n + 1);
            return n;
        }
    }
    out[0] = 0;
    return 0;
}

static int64_t seed = 2108;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char lists[200][WORDS][LEN + 1];
    for (int l = 0; l < 200; l++) {
        for (int w = 0; w < WORDS; w++) {
            int64_t letters[LEN];
            for (int i = 0; i < 50; i++) letters[i] = next_random() % 26;
            for (int i = 0; i < 50; i++) letters[50 + i] = letters[49 - i];
            if (next_random() % 200 != 0) {
                int64_t at = 25 + next_random() % 50;
                letters[at] = (letters[at] + 1 + next_random() % 25) % 26;
            }
            for (int i = 0; i < LEN; i++) lists[l][w][i] = (char)('a' + letters[i]);
            lists[l][w][LEN] = 0;
        }
    }
    int64_t found = 0, letters_total = 0, check = 0;
    char got[LEN + 1];
    for (int r = 0; r < 50; r++) {
        for (int l = 0; l < 200; l++) {
            int64_t n = first_palindrome(lists[l], got);
            if (n > 0) found++;
            letters_total += n;
            for (int i = 0; i < n && i < 3; i++) check = (check * 31 + got[i]) % 1000000007;
            check = (check * 31 + n) % 1000000007;
        }
    }
    printf("10000 searches: %lld found, %lld letters, checksum %lld\n", (long long)found,
           (long long)letters_total, (long long)check);
    return 0;
}
