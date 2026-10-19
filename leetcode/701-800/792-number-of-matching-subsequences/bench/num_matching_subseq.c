// LeetCode 792 — Number of Matching Subsequences: the bench, in C.
// Mirrors num_matching_subseq.kara: every word waits in the bucket of
// the next letter it needs, and s is walked once; a bucket is taken
// whole, left empty, and walked.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t w, matched;
} Wait;

typedef struct {
    Wait *items;
    int64_t len, cap;
} Bucket;

static void push(Bucket *b, int64_t w, int64_t matched) {
    if (b->len == b->cap) {
        b->cap = b->cap ? b->cap * 2 : 4;
        b->items = realloc(b->items, b->cap * sizeof(Wait));
    }
    b->items[b->len].w = w;
    b->items[b->len].matched = matched;
    b->len++;
}

static int64_t num_matching_subseq(const char *s, char **words, const int64_t *lens, int64_t n) {
    Bucket waiting[26];
    memset(waiting, 0, sizeof waiting);
    for (int64_t i = 0; i < n; i++) push(&waiting[words[i][0] - 'a'], i, 0);
    int64_t count = 0;
    for (const char *p = s; *p; p++) {
        Bucket moving = waiting[*p - 'a'];
        memset(&waiting[*p - 'a'], 0, sizeof(Bucket));
        for (int64_t k = 0; k < moving.len; k++) {
            int64_t w = moving.items[k].w, matched = moving.items[k].matched;
            if (matched + 1 == lens[w])
                count++;
            else
                push(&waiting[words[w][matched + 1] - 'a'], w, matched + 1);
        }
        free(moving.items);
    }
    for (int c = 0; c < 26; c++) free(waiting[c].items);
    return count;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char *random_word(int64_t *seed, int64_t len, int64_t letters) {
    char *word = malloc(len + 1);
    for (int64_t i = 0; i < len; i++) word[i] = (char)(97 + next_random(seed) % letters);
    word[len] = 0;
    return word;
}

int main(void) {
    int64_t seed = 792;
    static char *strings[16];
    for (int k = 0; k < 16; k++) {
        int64_t letters = 13 + next_random(&seed) % 14;
        strings[k] = random_word(&seed, 50000, letters);
    }
    static char *lists[64][5000];
    static int64_t lens[64][5000];
    for (int k = 0; k < 64; k++)
        for (int i = 0; i < 5000; i++) {
            int64_t len = 1 + next_random(&seed) % 50;
            lists[k][i] = random_word(&seed, len, 26);
            lens[k][i] = len;
        }
    int64_t rounds = 4000, total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t count = num_matching_subseq(strings[r % 16], lists[(r / 16) % 64], lens[(r / 16) % 64], 5000);
        total += count;
        check = (check * 131 + count + 1) % 1000000007;
    }
    printf("%lld rounds of 5000 words: %lld matching, checksum %lld\n", (long long)rounds, (long long)total,
           (long long)check);
    return 0;
}
