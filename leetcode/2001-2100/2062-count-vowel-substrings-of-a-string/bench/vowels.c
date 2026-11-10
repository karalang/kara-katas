// LeetCode #2062: Count Vowel Substrings of a String -- C mirror of the ★
// arm's benchmark (vowels.kara): 20000 words of 100 letters, each a vowel
// with chance 90 in 100, else one of `xyz`; the vowels met from each start
// kept as a set of five flags, cleared per start.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

static int vowel_slot(char c) {
    const char *p = strchr("aeiou", c);
    return (c != 0 && p) ? (int)(p - "aeiou") : -1;
}

static int64_t count_vowel_substrings(const char *word, int n) {
    int64_t count = 0;
    for (int i = 0; i < n; i++) {
        char met[5] = {0};
        int size = 0;
        for (int j = i; j < n; j++) {
            int v = vowel_slot(word[j]);
            if (v < 0) break;
            if (!met[v]) {
                met[v] = 1;
                size++;
            }
            if (size == 5) count++;
        }
    }
    return count;
}

static int64_t seed = 2062;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    char word[101];
    int64_t total = 0, check = 0;
    for (int t = 0; t < 20000; t++) {
        for (int k = 0; k < 100; k++) {
            if (next_random() % 100 < 90)
                word[k] = "aeiou"[next_random() % 5];
            else
                word[k] = "xyz"[next_random() % 3];
        }
        word[100] = 0;
        int64_t a = count_vowel_substrings(word, 100);
        total += a;
        check = (check * 31 + a) % 1000000007;
    }
    printf("20000 words: sum %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
