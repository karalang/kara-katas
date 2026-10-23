// LeetCode #884 bench: C mirror of uncommon_from_sentences.kara (the ★
// arm, one map of counts) on the same 1000 sentences. C has no map, so a
// hash table is written out here: open addressing over 512 slots, keyed
// by FNV-1a, each key a copy of the word as the Kara program's map keeps
// one, and the answer a list of copies.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 512

typedef struct { char *word; size_t len; int64_t n; } Slot;

static Slot table[SLOTS];

static uint64_t fnv(const char *s, size_t len) {
    uint64_t h = 1469598103934665603ULL;
    for (size_t k = 0; k < len; k++) { h ^= (unsigned char)s[k]; h *= 1099511628211ULL; }
    return h;
}

static void count_words(const char *s) {
    const char *p = s;
    for (;;) {
        const char *q = strchr(p, ' ');
        size_t len = q ? (size_t)(q - p) : strlen(p);
        size_t at = fnv(p, len) & (SLOTS - 1);
        while (table[at].word && !(table[at].len == len && memcmp(table[at].word, p, len) == 0))
            at = (at + 1) & (SLOTS - 1);
        if (table[at].word) {
            table[at].n += 1;
        } else {
            table[at].word = malloc(len + 1);
            memcpy(table[at].word, p, len);
            table[at].word[len] = 0;
            table[at].len = len;
            table[at].n = 1;
        }
        if (!q) break;
        p = q + 1;
    }
}

// the uncommon words, each a fresh copy, into out; returns how many
static int uncommon_from_sentences(const char *s1, const char *s2, char **out) {
    count_words(s1);
    count_words(s2);
    int k = 0;
    for (int at = 0; at < SLOTS; at++) {
        if (table[at].word) {
            if (table[at].n == 1) {
                out[k] = malloc(table[at].len + 1);
                memcpy(out[k], table[at].word, table[at].len + 1);
                k++;
            }
            free(table[at].word);
            table[at].word = NULL;
        }
    }
    return k;
}

static int64_t seed = 884;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

// up to 200 characters, words of 1 to 4 of the letters a to e
static char *sentence(void) {
    char *out = malloc(201);
    size_t len = 0;
    for (;;) {
        char word[5];
        int size = next_random() % 4 + 1;
        for (int k = 0; k < size; k++) word[k] = 97 + next_random() % 5;
        if (len == 0) {
            memcpy(out, word, size);
            len = size;
        } else if (len + 1 + size <= 200) {
            out[len] = ' ';
            memcpy(out + len + 1, word, size);
            len += 1 + size;
        } else {
            break;
        }
        if (next_random() % 80 == 0) break;
    }
    out[len] = 0;
    return out;
}

// the same for a word wherever it sits in the answer
static int64_t word_hash(const char *w) {
    int64_t h = 7;
    for (; *w; w++) h = (h * 131 + (unsigned char)*w) % 1000000007;
    return h;
}

int main(void) {
    char *sentences[1000];
    for (int i = 0; i < 1000; i++) sentences[i] = sentence();
    char *words[SLOTS];
    int64_t total = 0, check = 0;
    for (int r = 0; r < 200; r++) {
        for (int i = 0; i < 1000; i++) {
            int k = uncommon_from_sentences(sentences[i], sentences[(i + r + 1) % 1000], words);
            total += k;
            for (int j = 0; j < k; j++) {
                check = (check + word_hash(words[j])) % 1000000007;
                free(words[j]);
            }
        }
    }
    printf("1000 sentences, each paired with 200 others: %lld uncommon words, checksum %lld\n", (long long)total, (long long)check);
    for (int i = 0; i < 1000; i++) free(sentences[i]);
    return 0;
}
