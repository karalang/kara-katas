// LeetCode #1332 bench, C mirror of the Kāra bench: the ★ arm on 1000
// strings of 1000 letters built once, then 500 passes, each setting one
// letter of one string from the checksum so far, rebuilding that string,
// and answering every string.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int remove_palindrome_sub(const char *s, size_t n) {
    for (size_t i = 0; i < n / 2; i++) {
        if (s[i] != s[n - 1 - i]) {
            return 2;
        }
    }
    return 1;
}

static int64_t seed = 1332;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t count = 1000;
    const int64_t n = 1000;
    char **letters = malloc(sizeof(char *) * count);
    char **strings = malloc(sizeof(char *) * count);
    for (int64_t t = 0; t < count; t++) {
        char *row = malloc(n);
        memset(row, 'a', n);
        for (int64_t i = 0; i < n / 2; i++) {
            char c = next_random() % 2 == 0 ? 'a' : 'b';
            row[i] = c;
            row[n - 1 - i] = c;
        }
        if (t % 2 == 1) {
            int64_t k = n / 2 - 1 - t % 3;
            row[k] = row[k] == 'a' ? 'b' : 'a';
        }
        char *s = malloc(n);
        memcpy(s, row, n);
        strings[t] = s;
        letters[t] = row;
    }
    int64_t check = 0;
    for (int64_t pass = 0; pass < 500; pass++) {
        int64_t t = check % count;
        int64_t at = check / count % n;
        char c = check / 7 % 2 == 0 ? 'a' : 'b';
        letters[t][at] = c;
        if (pass % 2 == 0) {
            letters[t][n - 1 - at] = c;
        }
        free(strings[t]);
        strings[t] = malloc(n);
        memcpy(strings[t], letters[t], n);
        for (int64_t k = 0; k < count; k++) {
            check = (check * 31 + remove_palindrome_sub(strings[k], n) + pass) % 1000000007;
        }
    }
    printf("500 passes over 1000 strings of 1000 letters: checksum %lld\n", (long long)check);
    for (int64_t t = 0; t < count; t++) {
        free(letters[t]);
        free(strings[t]);
    }
    free(letters);
    free(strings);
    return 0;
}
