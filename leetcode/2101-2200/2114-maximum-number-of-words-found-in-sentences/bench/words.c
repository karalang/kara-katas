// LeetCode #2114: Maximum Number of Words Found in Sentences -- the
// benchmark, the same algorithm as words.kara: each sentence's spaces
// counted over its bytes, plus one, and the largest taken.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *s;
    size_t len, cap;
} str;

static void push(str *t, char c) {
    if (t->len == t->cap) {
        t->cap = t->cap ? t->cap * 2 : 16;
        t->s = realloc(t->s, t->cap);
    }
    t->s[t->len++] = c;
}

static int64_t most_words_found(const str *sentences, int n) {
    int64_t most = 0;
    for (int i = 0; i < n; i++) {
        int64_t words = 1;
        for (size_t k = 0; k < sentences[i].len; k++)
            if (sentences[i].s[k] == ' ') words++;
        if (words > most) most = words;
    }
    return most;
}

static int64_t seed = 2114;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static str lists[200][100];
    for (int a = 0; a < 200; a++) {
        for (int i = 0; i < 100; i++) {
            str *t = &lists[a][i];
            int64_t words = next_random() % 25 + 1;
            for (int64_t w = 0; w < words; w++) {
                if (w > 0) push(t, ' ');
                int64_t n = next_random() % 6 + 1;
                for (int64_t k = 0; k < n; k++) push(t, (char)('a' + next_random() % 26));
            }
        }
    }
    int64_t total = 0, check = 0;
    for (int round = 0; round < 10; round++) {
        for (int a = 0; a < 200; a++) {
            str *t = &lists[a][(round * 37 + a) % 100];
            push(t, ' ');
            push(t, 'a');
            int64_t got = most_words_found(lists[a], 100);
            total += got;
            check = (check * 31 + got) % 1000000007;
        }
    }
    printf("2000 solves: %lld words, checksum %lld\n", (long long)total, (long long)check);
    for (int a = 0; a < 200; a++)
        for (int i = 0; i < 100; i++) free(lists[a][i].s);
    return 0;
}
