// LeetCode #1768: Merge Strings Alternately -- the bench in C, mirroring
// merge_alternately.kara: one index walking both words into a new buffer.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static char *merge_alternately(const char *word1, const char *word2) {
    size_t n1 = strlen(word1), n2 = strlen(word2);
    char *merged = malloc(n1 + n2 + 1);
    size_t k = 0;
    for (size_t i = 0; i < (n1 > n2 ? n1 : n2); i++) {
        if (i < n1) merged[k++] = word1[i];
        if (i < n2) merged[k++] = word2[i];
    }
    merged[k] = 0;
    return merged;
}

static long long seed = 1768;
static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static char *words[1000];
    for (int w = 0; w < 1000; w++) {
        long long n = 1 + next_random() % 100;
        words[w] = malloc(n + 1);
        for (long long i = 0; i < n; i++) words[w][i] = (char)(97 + next_random() % 26);
        words[w][n] = 0;
    }
    long long check = 0;
    for (long long call = 0; call < 2000000; call++) {
        long long a = (check + call * 7919) % 1000;
        long long b = (check / 3 + call * 104729) % 1000;
        char *merged = merge_alternately(words[a], words[b]);
        long long len = (long long)strlen(merged);
        long long at = check % len;
        check = (check * 31 + len + (unsigned char)merged[at]) % 1000000007;
        free(merged);
    }
    printf("2000000 calls over 1000 words: checksum %lld\n", check);
    return 0;
}
