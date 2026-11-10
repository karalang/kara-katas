// LeetCode #2063: Vowels of All Substrings -- C mirror of the ★ arm's
// benchmark (vowels.kara): one text of 140000 letters, each a vowel with
// chance 40 in 100, and 200 windows of 100000 letters cut from it at a
// random place among its first 32768, each copied out and answered on its
// own.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t count_vowels(const char *word, int64_t n) {
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        if (word[i] && strchr("aeiou", word[i])) total += (i + 1) * (n - i);
    }
    return total;
}

static int64_t seed = 2063;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char text[140001];
    for (int k = 0; k < 140000; k++) {
        if (next_random() % 100 < 40)
            text[k] = "aeiou"[next_random() % 5];
        else
            text[k] = "bcdxyz"[next_random() % 6];
    }
    int64_t check = 0;
    for (int t = 0; t < 200; t++) {
        int64_t start = next_random();
        char *window = malloc(100001);
        memcpy(window, text + start, 100000);
        window[100000] = 0;
        int64_t a = count_vowels(window, 100000);
        free(window);
        check = (check * 31 + a % 1000000007) % 1000000007;
    }
    printf("200 windows: checksum %lld\n", (long long)check);
    return 0;
}
