// LeetCode #692: Top K Frequent Words -- bench program, C mirror of the select arm.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long long seed = 692;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int by_word(const void *a, const void *b) {
    return strcmp(*(char *const *)a, *(char *const *)b);
}

// Writes the top k into out; the words themselves are not copied.
static void top_k_frequent(char **words, int n, int k, char **out) {
    char **sorted = malloc(sizeof(char *) * n);
    memcpy(sorted, words, sizeof(char *) * n);
    qsort(sorted, n, sizeof(char *), by_word);
    char **distinct = malloc(sizeof(char *) * n);
    long long *counts = malloc(sizeof(long long) * n);
    int d = 0;
    for (int i = 0; i < n;) {
        int j = i;
        while (j < n && strcmp(sorted[j], sorted[i]) == 0) j++;
        distinct[d] = sorted[i];
        counts[d++] = j - i;
        i = j;
    }
    for (int r = 0; r < k; r++) {
        int pick = -1;
        for (int x = 0; x < d; x++)
            if (counts[x] > 0 && (pick < 0 || counts[x] > counts[pick])) pick = x;
        out[r] = distinct[pick];
        counts[pick] = 0;
    }
    free(sorted);
    free(distinct);
    free(counts);
}

int main(void) {
    static char store[100][500][5];
    static char *lists[100][500];
    for (int l = 0; l < 100; l++)
        for (int i = 0; i < 500; i++) {
            int len = 1 + (int)(next_random() % 4);
            for (int c = 0; c < len; c++) store[l][i][c] = (char)('a' + next_random() % 6);
            store[l][i][len] = 0;
            lists[l][i] = store[l][i];
        }
    int rounds = 60;
    long long checksum = 0, answers = 0;
    char *out[10];
    for (int r = 0; r < rounds; r++)
        for (int l = 0; l < 100; l++) {
            top_k_frequent(lists[l], 500, 10, out);
            for (int x = 0; x < 10; x++) {
                for (const char *p = out[x]; *p; p++) checksum = (checksum * 31 + *p) % 1000000007;
                checksum = (checksum * 31 + 1) % 1000000007;
                answers++;
            }
        }
    printf("%d rounds of 100 lists of 500 words: %lld words answered, checksum %lld\n", rounds, answers, checksum);
    return 0;
}
