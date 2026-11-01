// LeetCode #1032: Stream of Characters -- bench
// Mirrors ./stream_checker.kara; see ../README.md § Benchmarks.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t (*next)[26];
    unsigned char *end;
    int64_t nodes, cap;
    int64_t *stream;
    int64_t len;
} StreamChecker;

static int64_t add_node(StreamChecker *s) {
    if (s->nodes == s->cap) {
        s->cap *= 2;
        s->next = realloc(s->next, sizeof(int64_t[26]) * s->cap);
        s->end = realloc(s->end, s->cap);
    }
    for (int k = 0; k < 26; k++) s->next[s->nodes][k] = -1;
    s->end[s->nodes] = 0;
    return s->nodes++;
}

static void checker_new(StreamChecker *s, char **words, int count, int64_t stream_cap) {
    s->cap = 1024;
    s->nodes = 0;
    s->next = malloc(sizeof(int64_t[26]) * s->cap);
    s->end = malloc(s->cap);
    add_node(s);
    for (int w = 0; w < count; w++) {
        int64_t node = 0;
        for (int i = (int)strlen(words[w]) - 1; i >= 0; i--) {
            int k = words[w][i] - 'a';
            if (s->next[node][k] == -1) {
                int64_t child = add_node(s);
                s->next[node][k] = child;
            }
            node = s->next[node][k];
        }
        s->end[node] = 1;
    }
    s->stream = malloc(sizeof(int64_t) * stream_cap);
    s->len = 0;
}

static int query(StreamChecker *s, char letter) {
    s->stream[s->len++] = letter - 'a';
    int64_t node = 0;
    for (int64_t i = s->len - 1; i >= 0; i--) {
        node = s->next[node][s->stream[i]];
        if (node == -1) return 0;
        if (s->end[node]) return 1;
    }
    return 0;
}

static void checker_free(StreamChecker *s) {
    free(s->next);
    free(s->end);
    free(s->stream);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static char *random_text(int64_t *seed, int64_t len) {
    char *s = malloc(len + 1);
    for (int64_t i = 0; i < len; i++) s[i] = (char)(97 + next_random(seed) % 2);
    s[len] = 0;
    return s;
}

int main(void) {
    const int rounds = 50;
    int64_t seed = 1032;
    char *words[2000];
    for (int w = 0; w < 2000; w++) {
        int64_t len = 50 + next_random(&seed) % 151;
        words[w] = random_text(&seed, len);
    }
    char *stream = random_text(&seed, 40000);
    int64_t found = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        StreamChecker checker;
        checker_new(&checker, words, 2000, 40000);
        for (int i = 0; i < 40000; i++) {
            int hit = query(&checker, stream[i]);
            found += hit;
            check = (check * 3 + hit + 1) % 1000000007;
        }
        checker_free(&checker);
    }
    printf("2000 words, 40000 queries, %d rounds: %lld found, checksum %lld\n", rounds, (long long)found,
           (long long)check);
    return 0;
}
