// LeetCode #648: Replace Words -- C mirror of the Kāra bench.
//
// The ★ arm over the same inputs and rounds: a trie of the roots as a
// growing array of 26-entry child tables, each word walked until the
// first root ends. The sentence is scanned in place for spaces and the
// answer written into one buffer, so no word is copied on its own.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t next[26];
    int end;
} Node;

static char *replace_words(char **dictionary, int64_t roots, const char *sentence, int64_t length) {
    int64_t cap = 1024, count = 1;
    Node *trie = calloc(cap, sizeof(Node));
    for (int64_t r = 0; r < roots; r++) {
        int64_t node = 0;
        for (const char *p = dictionary[r]; *p; p++) {
            int c = *p - 'a';
            if (trie[node].next[c] == 0) {
                if (count == cap) {
                    trie = realloc(trie, 2 * cap * sizeof(Node));
                    memset(trie + cap, 0, cap * sizeof(Node));
                    cap *= 2;
                }
                trie[node].next[c] = count++;
            }
            node = trie[node].next[c];
        }
        trie[node].end = 1;
    }
    char *out = malloc(length + 1);
    int64_t o = 0, start = 0;
    while (start <= length) {
        int64_t stop = start;
        while (stop < length && sentence[stop] != ' ') stop++;
        int64_t node = 0, k = 0;
        while (start + k < stop && !trie[node].end) {
            node = trie[node].next[sentence[start + k] - 'a'];
            if (node == 0) break;
            k++;
        }
        int64_t keep = (node != 0 && trie[node].end) ? k : stop - start;
        if (start > 0) out[o++] = ' ';
        memcpy(out + o, sentence + start, keep);
        o += keep;
        start = stop + 1;
    }
    out[o] = 0;
    free(trie);
    return out;
}

static int64_t seed = 648;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t random_word(char *s, int64_t shortest, int64_t longest, int64_t letters) {
    int64_t n = shortest + next_random() % (longest - shortest + 1);
    for (int64_t i = 0; i < n; i++) s[i] = (char)(97 + next_random() % letters);
    s[n] = 0;
    return n;
}

int main(void) {
    enum { INPUTS = 20, ROUNDS = 100, ROOTS = 1000, WORDS = 20000 };
    char **dictionaries[INPUTS];
    char *sentences[INPUTS];
    int64_t lengths[INPUTS];
    for (int i = 0; i < INPUTS; i++) {
        int64_t letters = 3 + next_random() % 6;
        dictionaries[i] = malloc(ROOTS * sizeof(char *));
        for (int j = 0; j < ROOTS; j++) {
            dictionaries[i][j] = malloc(7);
            random_word(dictionaries[i][j], 3, 6, letters);
        }
        char *s = malloc(WORDS * 11);
        int64_t n = 0;
        for (int j = 0; j < WORDS; j++) {
            if (j > 0) s[n++] = ' ';
            n += random_word(s + n, 1, 10, letters);
        }
        sentences[i] = s;
        lengths[i] = n;
    }
    int64_t total = 0, checksum = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        int64_t i = (r * 7) % INPUTS;
        char *out = replace_words(dictionaries[i], ROOTS, sentences[i], lengths[i]);
        for (char *p = out; *p; p++) {
            total++;
            checksum = (checksum * 31 + *p) % 1000000007;
        }
        free(out);
    }
    printf("%d inputs, %d rounds: %lld characters, checksum %lld\n", INPUTS, ROUNDS, (long long)total, (long long)checksum);
    for (int i = 0; i < INPUTS; i++) {
        for (int j = 0; j < ROOTS; j++) free(dictionaries[i][j]);
        free(dictionaries[i]);
        free(sentences[i]);
    }
    return 0;
}
