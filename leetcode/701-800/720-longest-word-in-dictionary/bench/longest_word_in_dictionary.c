// LeetCode #720: Longest Word in Dictionary -- a trie, walked through
// word ends only. Benchmark mirror of the Kara trie arm: every word put
// in a trie with one array of 26 children per node, then a depth-first
// walk that steps only onto nodes where a word ends.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

typedef struct {
    int64_t **next;
    int64_t *word_at;
    int64_t len, cap;
} Trie;

static void add_node(Trie *t) {
    if (t->len == t->cap) {
        t->cap = t->cap ? t->cap * 2 : 16;
        t->next = realloc(t->next, t->cap * sizeof(int64_t *));
        t->word_at = realloc(t->word_at, t->cap * sizeof(int64_t));
    }
    t->next[t->len] = calloc(26, sizeof(int64_t));
    t->word_at[t->len] = -1;
    t->len++;
}

typedef struct { int64_t depth, word; } Found;

static Found deepest(const Trie *t, int64_t node, int64_t depth) {
    Found best = {depth, t->word_at[node]};
    for (int c = 0; c < 26; c++) {
        int64_t child = t->next[node][c];
        if (child != 0 && t->word_at[child] >= 0) {
            Found got = deepest(t, child, depth + 1);
            if (got.depth > best.depth) best = got;
        }
    }
    return best;
}

// Returns the length of the answer (the bench sums lengths).
static int64_t longest_word(char **words, int64_t n) {
    Trie t = {0};
    add_node(&t);
    for (int64_t i = 0; i < n; i++) {
        int64_t node = 0;
        for (const char *p = words[i]; *p; p++) {
            int64_t c = *p - 'a';
            if (t.next[node][c] == 0) {
                t.next[node][c] = t.len;
                add_node(&t);
            }
            node = t.next[node][c];
        }
        t.word_at[node] = i;
    }
    Found found = deepest(&t, 0, 0);
    int64_t len = found.word < 0 ? 0 : (int64_t)strlen(words[found.word]);
    for (int64_t i = 0; i < t.len; i++) free(t.next[i]);
    free(t.next);
    free(t.word_at);
    return len;
}

enum { DICTS = 40, WORDS = 1000 };

int main(void) {
    int64_t seed = 720;
    static char *dicts[DICTS][WORDS];
    for (int d = 0; d < DICTS; d++) {
        for (int64_t k = 0; k < WORDS; k++) {
            char *w = calloc(32, 1);
            if (k > 0 && next_random(&seed) % 4 != 0) {
                strcpy(w, dicts[d][next_random(&seed) % k]);
                size_t len = strlen(w);
                if (len < 30) w[len] = (char)(97 + next_random(&seed) % 4);
            } else {
                int64_t n = 1 + next_random(&seed) % 3;
                for (int64_t j = 0; j < n; j++) w[j] = (char)(97 + next_random(&seed) % 4);
            }
            dicts[d][k] = w;
        }
    }
    int64_t sum = 0;
    for (int64_t round = 0; round < 300; round++) {
        for (int64_t d = 0; d < DICTS; d++) {
            int64_t i = (round * 7919 + d * 104729) % WORDS;
            size_t len = strlen(dicts[d][i]);
            if (len < 30) dicts[d][i][len] = (char)(97 + round % 4);
            sum += longest_word(dicts[d], WORDS);
        }
    }
    printf("300 rounds of 40 dictionaries of 1000 words: sum %lld\n", (long long)sum);
    return 0;
}
