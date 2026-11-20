// LeetCode #1698: Number of Distinct Substrings in a String -- the bench's
// C mirror: the ★ arm on 100 random strings of 500 letters, each from the
// first 2 to 26 letters of the alphabet, all drawn first, each answered 3
// times. The trie's nodes are rows of 26 children in one growable array.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define COUNT 100
#define ROUNDS 3
#define N 500

typedef struct {
    int64_t next[26];
} node;

static int32_t count_distinct(const char *s, int64_t n) {
    int64_t cap = 1024, len = 1;
    node *children = calloc((size_t)cap, sizeof *children);
    int32_t made = 0;
    for (int64_t start = 0; start < n; start++) {
        int64_t at = 0;
        for (int64_t i = start; i < n; i++) {
            int64_t edge = s[i] - 'a';
            if (children[at].next[edge] == 0) {
                if (len == cap) {
                    cap *= 2;
                    children = realloc(children, (size_t)cap * sizeof *children);
                }
                memset(&children[len], 0, sizeof *children);
                len++;
                children[at].next[edge] = len - 1;
                made++;
            }
            at = children[at].next[edge];
        }
    }
    free(children);
    return made;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1698;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const char *alphabet = "abcdefghijklmnopqrstuvwxyz";
    static char strings[COUNT][N];
    for (int c = 0; c < COUNT; c++) {
        int64_t used = next_random() % 25 + 2;
        for (int i = 0; i < N; i++) {
            strings[c][i] = alphabet[next_random() % used];
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t answer = count_distinct(strings[c], N);
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d strings of %d letters, %d rounds: answers sum to %lld, checksum %lld\n", COUNT, N, ROUNDS, (long long)total, (long long)check);
    return 0;
}
