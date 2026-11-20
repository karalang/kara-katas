// LeetCode #1239: the benchmark, mirroring the Kāra file.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LISTS 20000
#define WORDS 16

static long long seed = 1239;

static long long next_random(void) {
    seed = (seed * 1103515245LL + 12345) % 2147483648LL;
    return seed / 65536;
}

// -1 for a word that repeats a letter.
static long long mask_of(const char *word) {
    long long mask = 0;
    for (const char *p = word; *p; p++) {
        long long bit = 1LL << (*p - 97);
        if (mask & bit) return -1;
        mask |= bit;
    }
    return mask;
}

static long long search(const long long *masks, int n, int at, long long taken) {
    if (at == n) return __builtin_popcountll(taken);
    long long best = search(masks, n, at + 1, taken);
    if ((taken & masks[at]) == 0) {
        long long t = search(masks, n, at + 1, taken | masks[at]);
        if (t > best) best = t;
    }
    return best;
}

static long long max_length(char **arr, int count) {
    long long *masks = malloc(sizeof(long long) * count);
    int n = 0;
    for (int i = 0; i < count; i++) {
        long long m = mask_of(arr[i]);
        if (m >= 0) masks[n++] = m;
    }
    long long r = search(masks, n, 0, 0);
    free(masks);
    return r;
}

int main(void) {
    char ***lists = malloc(sizeof(char **) * LISTS);
    for (int l = 0; l < LISTS; l++) {
        lists[l] = malloc(sizeof(char *) * WORDS);
        for (int k = 0; k < WORDS; k++) {
            int len = (int)(next_random() % 2 + 1);
            char *w = malloc(len + 1);
            for (int i = 0; i < len; i++) w[i] = (char)('a' + next_random() % 26);
            w[len] = 0;
            lists[l][k] = w;
        }
    }
    long long total = 0, check = 0;
    for (int l = 0; l < LISTS; l++) {
        long long best = max_length(lists[l], WORDS);
        total += best;
        check = (check * 131 + best) % 1000000007;
    }
    printf("20000 lists of 16 words: total %lld, checksum %lld\n", total, check);
    return 0;
}
