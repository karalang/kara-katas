// LeetCode #1268 bench, in C: the ★ arm (the products sorted, a binary
// search for each prefix typed, and up to three products from there that
// start with it) on 100 random lists of 1000 words of 1 to 10 letters from
// `a` to `d` built once, each searched for its own 20-letter word, 100
// rounds; every suggestion folded into a checksum.
// The sort orders a copy of the array of pointers, and a suggestion is a
// pointer to its product.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int cmp(const void *a, const void *b) { return strcmp(*(char *const *)a, *(char *const *)b); }

// out[e * 3 + k] is the k-th suggestion after e + 1 letters; counts[e] how many.
static void suggested_products(char **products, int n, const char *search, char **out, int *counts) {
    char **sorted = malloc(n * sizeof(char *));
    memcpy(sorted, products, n * sizeof(char *));
    qsort(sorted, n, sizeof(char *), cmp);
    int len = strlen(search);
    for (int end = 1; end <= len; end++) {
        int lo = 0, hi = n;
        while (lo < hi) {
            int mid = (lo + hi) / 2;
            // the product against the prefix of `end` letters
            int c = strncmp(sorted[mid], search, end);
            if (c < 0) lo = mid + 1;
            else hi = mid;
        }
        int k = 0;
        for (int i = lo; i < n && k < 3 && strncmp(sorted[i], search, end) == 0; i++) out[(end - 1) * 3 + k++] = sorted[i];
        counts[end - 1] = k;
    }
    free(sorted);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1268;
    static char *lists[100][1000];
    static char searches[100][21];
    for (int l = 0; l < 100; l++) {
        for (int i = 0; i < 1000; i++) {
            int len = next_random(&seed) % 10 + 1;
            char *w = malloc(len + 1);
            for (int j = 0; j < len; j++) w[j] = 'a' + next_random(&seed) % 4;
            w[len] = 0;
            lists[l][i] = w;
        }
        for (int j = 0; j < 20; j++) searches[l][j] = 'a' + next_random(&seed) % 4;
        searches[l][20] = 0;
    }
    char *out[60];
    int counts[20];
    int64_t check = 0;
    for (int64_t round = 0; round < 100; round++)
        for (int l = 0; l < 100; l++) {
            suggested_products(lists[l], 1000, searches[l], out, counts);
            for (int e = 0; e < 20; e++) {
                check = (check * 131 + counts[e] + round) % 1000000007;
                for (int k = 0; k < counts[e]; k++)
                    for (const unsigned char *p = (const unsigned char *)out[e * 3 + k]; *p; p++)
                        check = (check * 131 + *p) % 1000000007;
            }
        }
    printf("100 rounds of 100 searches among 1000 words: checksum %lld\n", (long long)check);
    return 0;
}
