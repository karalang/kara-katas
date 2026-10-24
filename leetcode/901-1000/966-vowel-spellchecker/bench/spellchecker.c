// Benchmark: LeetCode #966 Vowel Spellchecker -- the ★ arm, three maps,
// on cases of 5000 words and 5000 queries, LeetCode's largest. Mirrors
// spellchecker.kara, .rs, .py and go-seq/. Each map is an open-addressing
// table of 16384 slots keyed by FNV-1a, built afresh on every call as the
// other languages build theirs; a slot holds the index of the word it
// maps to. Words are at most 7 letters, kept in 8-byte arrays.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define MAXW 5000
#define SLOTS 16384

typedef struct {
    char s[8];
} Word;

static uint64_t hash(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) h = (h ^ (unsigned char)*s) * 1099511628211ULL;
    return h;
}

static void lower(const char *w, char *out) {
    int i = 0;
    for (; w[i]; i++) out[i] = (w[i] >= 'A' && w[i] <= 'Z') ? w[i] + 32 : w[i];
    out[i] = 0;
}

static void devowel(const char *w, char *out) {
    lower(w, out);
    for (int i = 0; out[i]; i++)
        if (strchr("aeiou", out[i])) out[i] = '*';
}

// A table of keys, each slot -1 or the index of the key's first word.
typedef struct {
    Word key[SLOTS];
    int idx[SLOTS];
} Table;

static void clear(Table *t) { memset(t->idx, -1, sizeof t->idx); }

static int *slot(Table *t, const char *k) {
    uint64_t h = hash(k) & (SLOTS - 1);
    while (t->idx[h] >= 0 && strcmp(t->key[h].s, k) != 0) h = (h + 1) & (SLOTS - 1);
    return &t->idx[h];
}

static void put_first(Table *t, const char *k, int i) {
    int *p = slot(t, k);
    if (*p < 0) {
        *p = i;
        strcpy(t->key[p - t->idx].s, k);
    }
}

static int get(Table *t, const char *k) { return *slot(t, k); }

static Table exact, by_case, by_vowel;

static void spellchecker(Word *wordlist, int n, Word *queries, int m, Word *out) {
    clear(&exact);
    clear(&by_case);
    clear(&by_vowel);
    char k[8];
    for (int i = 0; i < n; i++) {
        put_first(&exact, wordlist[i].s, i);
        lower(wordlist[i].s, k);
        put_first(&by_case, k, i);
        devowel(wordlist[i].s, k);
        put_first(&by_vowel, k, i);
    }
    for (int j = 0; j < m; j++) {
        int i;
        if (get(&exact, queries[j].s) >= 0) {
            out[j] = queries[j];
            continue;
        }
        lower(queries[j].s, k);
        if ((i = get(&by_case, k)) >= 0) {
            out[j] = wordlist[i];
            continue;
        }
        devowel(queries[j].s, k);
        if ((i = get(&by_vowel, k)) >= 0) {
            out[j] = wordlist[i];
            continue;
        }
        out[j].s[0] = 0;
    }
}

static int64_t seed = 966;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static const char *ALPHABET = "aeioukbAEIOUKB";

static int random_word(int len, int *w) {
    for (int i = 0; i < len; i++) w[i] = next_random() % 14;
    return len;
}

static void spell(const int *letters, int len, Word *out) {
    for (int i = 0; i < len; i++) out->s[i] = ALPHABET[letters[i]];
    out->s[len] = 0;
}

static int64_t fold(const char *s, int64_t check) {
    int64_t h = check;
    for (; *s; s++) h = (h * 131 + (unsigned char)*s) % 1000000007;
    return (h * 131 + 1) % 1000000007;
}

static void random_case(int n, int m, int max_len, Word *wl, Word *qs) {
    static int ws[MAXW][8], lens[MAXW];
    for (int i = 0; i < n; i++) lens[i] = random_word(1 + next_random() % max_len, ws[i]);
    for (int j = 0; j < m; j++) {
        int k = next_random() % n;
        int q[8], len = lens[k];
        memcpy(q, ws[k], sizeof q);
        int kind = next_random() % 4;
        if (kind == 3) {
            len = random_word(1 + next_random() % max_len, q);
        } else {
            for (int i = 0; i < len; i++) {
                if (kind == 1 && next_random() % 2 == 0) {
                    q[i] = (q[i] + 7) % 14;
                } else if (kind == 2 && q[i] % 7 < 5 && next_random() % 2 == 0) {
                    int a = next_random() % 5;
                    q[i] = a + 7 * (next_random() % 2);
                }
            }
        }
        spell(q, len, &qs[j]);
    }
    for (int i = 0; i < n; i++) spell(ws[i], lens[i], &wl[i]);
}

static Word wls[5][MAXW], qss[5][MAXW], got[MAXW];

int main(void) {
    int rounds = 200;
    for (int c = 0; c < 5; c++) random_case(5000, 5000, 7, wls[c], qss[c]);
    int64_t matched = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        spellchecker(wls[r % 5], 5000, qss[r % 5], 5000, got);
        for (int j = 0; j < 5000; j++) {
            if (got[j].s[0]) matched++;
            check = fold(got[j].s, check);
        }
    }
    printf("%d rounds over 5 cases of 5000 words and 5000 queries: %lld matched, checksum %lld\n",
           rounds, (long long)matched, (long long)check);
    return 0;
}
