// LeetCode #2068: Check Whether Two Strings are Almost Equivalent -- C
// mirror of the ★ arm's benchmark (almost.kara): every pair of 1500 words
// of 100 letters, each a common word of `a`, `b` and `c` with up to 30
// letters changed.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static bool check_almost_equivalent(const char *word1, const char *word2) {
    int64_t diff[26] = {0};
    for (const char *p = word1; *p; p++) diff[*p - 'a']++;
    for (const char *p = word2; *p; p++) diff[*p - 'a']--;
    for (int c = 0; c < 26; c++)
        if (llabs(diff[c]) > 3) return false;
    return true;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const char letters[3] = {'a', 'b', 'c'};
    int64_t seed = 2068;
    char base[101];
    for (int i = 0; i < 100; i++) base[i] = letters[next_random(&seed) % 3];
    base[100] = 0;
    char(*words)[101] = malloc(1500 * sizeof *words);
    for (int w = 0; w < 1500; w++) {
        memcpy(words[w], base, 101);
        int64_t changes = next_random(&seed) % 31;
        for (int64_t k = 0; k < changes; k++) {
            int64_t i = next_random(&seed) % 100;
            words[w][i] = letters[next_random(&seed) % 3];
        }
    }
    int64_t yes = 0, check = 0;
    for (int64_t i = 0; i < 1500; i++)
        for (int64_t j = i + 1; j < 1500; j++)
            if (check_almost_equivalent(words[i], words[j])) {
                yes++;
                check = (check * 31 + i * 1500 + j) % 1000000007;
            }
    printf("1124250 pairs: %lld almost equivalent, checksum %lld\n", (long long)yes, (long long)check);
    free(words);
    return 0;
}
