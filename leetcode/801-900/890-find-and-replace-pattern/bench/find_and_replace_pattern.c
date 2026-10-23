// LeetCode #890 bench: the table arm (two tables of 26 letters) with every
// one of 6000 words of 10 letters taken in turn as the pattern for all
// 6000. The same algorithm as find_and_replace_pattern.kara; each kept
// word is copied, as the Kāra arm clones it.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define WORDS 6000
#define LEN 10

static int matches(const char *word, const char *pattern) {
    int64_t to[26], from[26];
    for (int i = 0; i < 26; i++) to[i] = from[i] = -1;
    for (int i = 0; i < LEN; i++) {
        int64_t a = pattern[i] - 97;
        int64_t b = word[i] - 97;
        if (to[a] < 0 && from[b] < 0) {
            to[a] = b;
            from[b] = a;
        } else if (to[a] != b || from[b] != a) {
            return 0;
        }
    }
    return 1;
}

// the kept words, copied into `out`; returns how many
static int64_t find_and_replace_pattern(char words[][LEN + 1], int64_t n, const char *pattern, char **out) {
    int64_t kept = 0;
    for (int64_t i = 0; i < n; i++) {
        if (matches(words[i], pattern)) {
            out[kept] = malloc(LEN + 1);
            memcpy(out[kept], words[i], LEN + 1);
            kept++;
        }
    }
    return kept;
}

static int64_t seed = 890;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static char words[WORDS][LEN + 1];
static char *out[WORDS];

int main(void) {
    for (int k = 0; k < WORDS; k++) {
        for (int i = 0; i < LEN; i++) words[k][i] = (char)(97 + next_random() % 3);
        words[k][LEN] = 0;
    }
    int64_t found = 0, check = 0;
    for (int k = 0; k < WORDS; k++) {
        int64_t kept = find_and_replace_pattern(words, WORDS, words[k], out);
        for (int64_t i = 0; i < kept; i++) free(out[i]);
        found += kept;
        check = (check * 131 + kept) % 1000000007;
    }
    printf("6000 patterns over 6000 words of 10 letters: %lld matches, checksum %lld\n", (long long)found, (long long)check);
    return 0;
}
