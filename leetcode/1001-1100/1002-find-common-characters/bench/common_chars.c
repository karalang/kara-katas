// Benchmark: LeetCode #1002 Find Common Characters -- the ★ arm, the
// least count of each letter, on lists of 100 words of 100 letters,
// LeetCode's largest. Mirrors common_chars.kara, .rs, .py and go-seq/.
// The answer is LeetCode's C shape: an array of malloc'd one-letter
// strings, freed by the caller.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char **common_chars(char **words, int words_size, int *return_size) {
    int64_t least[26];
    for (int i = 0; i < 26; i++) least[i] = 1000;
    for (int w = 0; w < words_size; w++) {
        int64_t count[26] = {0};
        for (const char *p = words[w]; *p; p++) count[*p - 'a']++;
        for (int i = 0; i < 26; i++)
            if (count[i] < least[i]) least[i] = count[i];
    }
    char **ans = malloc(sizeof(char *) * 100);
    int n = 0;
    for (int i = 0; i < 26; i++) {
        for (int64_t k = 0; k < least[i]; k++) {
            char *s = malloc(2);
            s[0] = (char)('a' + i);
            s[1] = 0;
            ans[n++] = s;
        }
    }
    *return_size = n;
    return ans;
}

static int64_t seed = 1002;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int rounds = 1000;
    // 20 lists of 100 words of 100 letters, list t drawing its letters
    // from the first 2 + t % 10 of the alphabet
    static char text[20][100][101];
    static char *lists[20][100];
    for (int t = 0; t < 20; t++) {
        int64_t alphabet = 2 + t % 10;
        for (int w = 0; w < 100; w++) {
            for (int k = 0; k < 100; k++) text[t][w][k] = (char)(97 + next_random() % alphabet);
            text[t][w][100] = 0;
            lists[t][w] = text[t][w];
        }
    }
    int64_t found = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < 20; i++) {
            int size;
            char **ans = common_chars(lists[(r + i) % 20], 100, &size);
            found += size;
            for (int k = 0; k < size; k++) {
                for (const char *p = ans[k]; *p; p++) check = (check * 31 + *p) % 1000000007;
                free(ans[k]);
            }
            free(ans);
        }
    }
    printf("%d rounds over 20 lists of 100 words of 100 letters: %lld common letters, checksum %lld\n",
           rounds, (long long)found, (long long)check);
    return 0;
}
