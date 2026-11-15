// LeetCode #2185: Counting Words With a Given Prefix -- the benchmark's C
// mirror of prefix_count.kara: each word, a pointer and a length, asked
// whether it is at least as long as the prefix and begins with it.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long long prefix_count(char **words, long long *lens, long long n, const char *pref, long long plen) {
    long long count = 0;
    for (long long i = 0; i < n; i++) {
        if (lens[i] >= plen && memcmp(words[i], pref, plen) == 0) count++;
    }
    return count;
}

static long long seed = 2185;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static void random_word(char *w, long long n) {
    for (long long i = 0; i < n; i++) w[i] = (char)(97 + next_random() % 2);
}

int main(void) {
    char *words[100];
    long long lens[100];
    for (int i = 0; i < 100; i++) {
        lens[i] = next_random() % 100 + 1;
        words[i] = malloc(lens[i]);
        random_word(words[i], lens[i]);
    }
    long long check = 0;
    char pref[8];
    for (int r = 0; r < 100000; r++) {
        long long plen = next_random() % 8 + 1;
        random_word(pref, plen);
        check = (check * 31 + prefix_count(words, lens, 100, pref, plen)) % 1000000007;
    }
    printf("100000 solves: checksum %lld\n", check);
    for (int i = 0; i < 100; i++) free(words[i]);
    return 0;
}
