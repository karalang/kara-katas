// LeetCode #2746: Decremental String Concatenation -- the bench
// (decremental.kara in C): the shortest string for each pair of first and
// last letters in a 26 by 26 array, rolled word by word.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NONE 1000000000LL
#define WORDS 1000

typedef struct {
    char text[WORDS][11];
    int64_t len[WORDS];
} List;

static int64_t minimize_concatenated_length(const List *words) {
    static int64_t best[26][26], next[26][26];
    for (int f = 0; f < 26; f++)
        for (int l = 0; l < 26; l++) best[f][l] = NONE;
    best[words->text[0][0] - 'a'][words->text[0][words->len[0] - 1] - 'a'] = words->len[0];
    for (int i = 1; i < WORDS; i++) {
        int64_t n = words->len[i];
        int a = words->text[i][0] - 'a', b = words->text[i][n - 1] - 'a';
        for (int f = 0; f < 26; f++)
            for (int l = 0; l < 26; l++) next[f][l] = NONE;
        for (int f = 0; f < 26; f++) {
            for (int l = 0; l < 26; l++) {
                int64_t length = best[f][l];
                if (length == NONE) continue;
                int64_t after = length + n - (l == a ? 1 : 0);
                if (after < next[f][b]) next[f][b] = after;
                int64_t before = length + n - (b == f ? 1 : 0);
                if (before < next[a][l]) next[a][l] = before;
            }
        }
        memcpy(best, next, sizeof best);
    }
    int64_t shortest = NONE;
    for (int f = 0; f < 26; f++)
        for (int l = 0; l < 26; l++)
            if (best[f][l] < shortest) shortest = best[f][l];
    return shortest;
}

static int64_t seed = 2746;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int count = 100, rounds = 5;
    List *lists = malloc(sizeof(List) * count);
    for (int k = 0; k < count; k++) {
        for (int i = 0; i < WORDS; i++) {
            int64_t len = next_random() % 10 + 1;
            for (int64_t j = 0; j < len; j++) lists[k].text[i][j] = (char)('a' + next_random() % 26);
            lists[k].text[i][len] = 0;
            lists[k].len[i] = len;
        }
    }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int k = 0; k < count; k++) {
            int64_t length = minimize_concatenated_length(&lists[k]);
            sum += length;
            check = (check * 31 + length + r) % 1000000007;
        }
    }
    printf("%d lists of 1000 words, %d rounds: lengths sum to %lld, checksum %lld\n", count, rounds, (long long)sum, (long long)check);
    free(lists);
    return 0;
}
