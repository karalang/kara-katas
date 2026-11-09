// Benchmark: LeetCode #1087 Brace Expansion -- mirrors brace_expansion.kara:
// the pattern read into sorted groups and the words built by a depth-first
// walk, each word copied into a fresh allocation as the Kāra arm's
// `word.clone()` is, over 2000 patterns built once.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char letters[26];
    int n;
} Group;

typedef struct {
    char **words;
    int64_t n, cap;
} Words;

static int64_t groups_of(const char *s, Group *groups) {
    int64_t ng = 0;
    Group *open = NULL;
    for (const char *p = s; *p; p++) {
        char c = *p;
        if (c == '{') {
            open = &groups[ng];
            open->n = 0;
        } else if (c == '}') {
            // insertion sort, the group is a handful of letters
            for (int i = 1; i < open->n; i++) {
                char x = open->letters[i];
                int j = i - 1;
                while (j >= 0 && open->letters[j] > x) {
                    open->letters[j + 1] = open->letters[j];
                    j--;
                }
                open->letters[j + 1] = x;
            }
            ng++;
            open = NULL;
        } else if (c == ',') {
        } else if (open) {
            open->letters[open->n++] = c;
        } else {
            groups[ng].letters[0] = c;
            groups[ng].n = 1;
            ng++;
        }
    }
    return ng;
}

static void walk(const Group *groups, int64_t ng, int64_t at, char *word, Words *out) {
    if (at == ng) {
        if (out->n == out->cap) {
            out->cap = out->cap ? out->cap * 2 : 4;
            out->words = realloc(out->words, sizeof(char *) * (size_t)out->cap);
        }
        char *w = malloc((size_t)at + 1);
        memcpy(w, word, (size_t)at + 1);
        out->words[out->n++] = w;
        return;
    }
    for (int i = 0; i < groups[at].n; i++) {
        word[at] = groups[at].letters[i];
        word[at + 1] = 0;
        walk(groups, ng, at + 1, word, out);
        word[at] = 0;
    }
}

static Words expand(const char *s) {
    Group groups[50];
    int64_t ng = groups_of(s, groups);
    char word[51] = {0};
    Words out = {0};
    walk(groups, ng, 0, word, &out);
    return out;
}

static int64_t seed = 1087;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static void random_pattern(char *s, int64_t most, int64_t k) {
    int64_t len = 0;
    s[0] = 0;
    int64_t parts = next_random() % 8 + 1;
    for (int64_t p = 0; p < parts; p++) {
        if (next_random() % 2 == 0) {
            char c = (char)('a' + next_random() % k);
            if (len + 1 <= most) {
                s[len++] = c;
                s[len] = 0;
            }
        } else {
            int64_t want = next_random() % k + 1;
            char letters[26];
            int64_t n = 0;
            while (n < want) {
                char c = (char)('a' + next_random() % k);
                int seen = 0;
                for (int64_t i = 0; i < n; i++) seen |= letters[i] == c;
                if (!seen) letters[n++] = c;
            }
            char group[64];
            int64_t g = 0;
            group[g++] = '{';
            for (int64_t i = 0; i < n; i++) {
                if (i) group[g++] = ',';
                group[g++] = letters[i];
            }
            group[g++] = '}';
            if (len + g <= most) {
                memcpy(s + len, group, (size_t)g);
                len += g;
                s[len] = 0;
            }
        }
    }
    if (len == 0) {
        s[0] = 'a';
        s[1] = 0;
    }
}

static char patterns[2000][51];

int main(void) {
    int64_t rounds = 400;
    for (int64_t t = 0; t < 2000; t++) random_pattern(patterns[t], 50, t % 6 + 1);
    int64_t words = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < 2000; i++) {
            Words out = expand(patterns[(r * 7 + i) % 2000]);
            words += out.n;
            const char *mid = out.words[out.n / 2];
            check = (check * 31 + out.n + (unsigned char)mid[strlen(mid) - 1]) % 1000000007;
            for (int64_t j = 0; j < out.n; j++) free(out.words[j]);
            free(out.words);
        }
    }
    printf("%lld rounds over 2000 patterns: %lld words, checksum %lld\n", (long long)rounds, (long long)words,
           (long long)check);
    return 0;
}
