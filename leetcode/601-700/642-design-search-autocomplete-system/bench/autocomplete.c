// Benchmark for #642: mirror of autocomplete.kara (the ★ arm: a trie
// searched below the prefix) on the same workload. As the Kāra builds a
// new String for each node it walks, this mallocs a new path for each
// child and frees it after.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t children[27];
    int64_t count;
} Node;

typedef struct {
    int64_t count;
    char *text;
} Found;

typedef struct {
    Found *items;
    size_t len, cap;
} FoundList;

typedef struct {
    Node *nodes;
    size_t len, cap;
    char typed[4096];
    size_t typed_len;
    int64_t at;
} AutocompleteSystem;

static int64_t branch(char c) { return c == ' ' ? 26 : c - 'a'; }

static char letter(int64_t b) { return b == 26 ? ' ' : (char)('a' + b); }

static int64_t new_node(AutocompleteSystem *s) {
    if (s->len == s->cap) {
        s->cap = s->cap ? s->cap * 2 : 64;
        s->nodes = realloc(s->nodes, s->cap * sizeof(Node));
    }
    for (int b = 0; b < 27; b++) {
        s->nodes[s->len].children[b] = -1;
    }
    s->nodes[s->len].count = 0;
    return (int64_t)s->len++;
}

static void gather(const Node *nodes, int64_t node, const char *path, size_t plen, FoundList *found) {
    if (nodes[node].count > 0) {
        if (found->len == found->cap) {
            found->cap = found->cap ? found->cap * 2 : 16;
            found->items = realloc(found->items, found->cap * sizeof(Found));
        }
        char *copy = malloc(plen + 1);
        memcpy(copy, path, plen + 1);
        found->items[found->len].count = nodes[node].count;
        found->items[found->len].text = copy;
        found->len++;
    }
    for (int64_t b = 0; b < 27; b++) {
        int64_t child = nodes[node].children[b];
        if (child != -1) {
            char *next = malloc(plen + 2);
            memcpy(next, path, plen);
            next[plen] = letter(b);
            next[plen + 1] = 0;
            gather(nodes, child, next, plen + 1, found);
            free(next);
        }
    }
}

static int by_rank(const void *x, const void *y) {
    const Found *a = x, *b = y;
    if (a->count != b->count) {
        return a->count > b->count ? -1 : 1;
    }
    return strcmp(a->text, b->text);
}

static void add(AutocompleteSystem *s, const char *sentence, size_t n, int64_t times) {
    int64_t node = 0;
    for (size_t i = 0; i < n; i++) {
        int64_t b = branch(sentence[i]);
        if (s->nodes[node].children[b] == -1) {
            int64_t fresh = new_node(s);
            s->nodes[node].children[b] = fresh;
        }
        node = s->nodes[node].children[b];
    }
    s->nodes[node].count += times;
}

static void system_init(AutocompleteSystem *s, char **sentences, int64_t *times, int n) {
    s->nodes = NULL;
    s->len = s->cap = 0;
    s->typed_len = 0;
    s->typed[0] = 0;
    s->at = 0;
    new_node(s);
    for (int i = 0; i < n; i++) {
        add(s, sentences[i], strlen(sentences[i]), times[i]);
    }
}

// The answer to one call, in `out` (owned by the caller, each name
// malloc'd); returns how many names.
static int input(AutocompleteSystem *s, char c, char **out) {
    if (c == '#') {
        add(s, s->typed, s->typed_len, 1);
        s->typed_len = 0;
        s->typed[0] = 0;
        s->at = 0;
        return 0;
    }
    s->typed[s->typed_len++] = c;
    s->typed[s->typed_len] = 0;
    if (s->at != -1) {
        s->at = s->nodes[s->at].children[branch(c)];
    }
    if (s->at == -1) {
        return 0;
    }
    FoundList found = {NULL, 0, 0};
    gather(s->nodes, s->at, s->typed, s->typed_len, &found);
    qsort(found.items, found.len, sizeof(Found), by_rank);
    int k = 0;
    for (size_t i = 0; i < found.len; i++) {
        if (i < 3) {
            out[k++] = found.items[i].text;
        } else {
            free(found.items[i].text);
        }
    }
    free(found.items);
    return k;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char *random_sentence(int64_t most, int64_t *seed) {
    int64_t length = 1 + next_random(seed) % most;
    char *s = malloc((size_t)length + 1);
    for (int64_t i = 0; i < length; i++) {
        s[i] = "abc "[next_random(seed) % 4];
    }
    s[length] = 0;
    return s;
}

typedef struct {
    char *sentences[100];
    int64_t times[100];
    char typing[5001];
} History;

int main(void) {
    int64_t seed = 642;
    static History histories[10];
    for (int h = 0; h < 10; h++) {
        History *hi = &histories[h];
        int n = 0;
        while (n < 100) {
            char *s = random_sentence(100, &seed);
            int seen = 0;
            for (int i = 0; i < n; i++) {
                if (strcmp(hi->sentences[i], s) == 0) {
                    seen = 1;
                }
            }
            if (seen) {
                free(s);
            } else {
                hi->sentences[n] = s;
                hi->times[n] = 1 + next_random(&seed) % 100;
                n++;
            }
        }
        size_t len = 0;
        char buf[5200];
        while (len < 5000) {
            if (next_random(&seed) % 2 == 0) {
                const char *s = hi->sentences[next_random(&seed) % 100];
                size_t l = strlen(s);
                memcpy(buf + len, s, l);
                len += l;
            } else {
                char *s = random_sentence(100, &seed);
                size_t l = strlen(s);
                memcpy(buf + len, s, l);
                len += l;
                free(s);
            }
            buf[len++] = '#';
        }
        memcpy(hi->typing, buf, 5000);
        hi->typing[5000] = 0;
    }
    int64_t rounds = 40;
    int64_t names = 0;
    int64_t checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        History *h = &histories[r % 10];
        AutocompleteSystem s;
        system_init(&s, h->sentences, h->times, 100);
        for (int i = 0; i < 5000; i++) {
            char *got[3];
            int k = input(&s, h->typing[i], got);
            for (int j = 0; j < k; j++) {
                int64_t len = (int64_t)strlen(got[j]);
                checksum = (checksum * 31 + len * 65536 + (int64_t)(unsigned char)got[j][0] * 256 +
                            (int64_t)(unsigned char)got[j][len - 1]) %
                           1000000007;
                names++;
                free(got[j]);
            }
            checksum = (checksum * 31 + 1) % 1000000007;
        }
        free(s.nodes);
    }
    printf("%lld rounds of 5000 calls: %lld names, checksum %lld\n", (long long)rounds, (long long)names,
           (long long)checksum);
    return 0;
}
