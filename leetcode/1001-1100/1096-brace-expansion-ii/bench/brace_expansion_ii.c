// Benchmark: LeetCode #1096 Brace Expansion II -- C mirror of
// brace_expansion_ii.kara: the stack arm, two lists of words sorted and
// deduplicated at each `}`, over 64 expressions of up to 60 characters
// built once, each round changing one letter in every expression. Each
// word is its own malloc'd string, as each is its own String in Kāra.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char **items;
    size_t len, cap;
} Words;

static void push(Words *w, char *s) {
    if (w->len == w->cap) {
        w->cap = w->cap ? w->cap * 2 : 4;
        w->items = realloc(w->items, w->cap * sizeof(char *));
    }
    w->items[w->len++] = s;
}

static char *concat2(const char *a, const char *b) {
    size_t la = strlen(a), lb = strlen(b);
    char *s = malloc(la + lb + 1);
    memcpy(s, a, la);
    memcpy(s + la, b, lb + 1);
    return s;
}

static void release(Words *w) {
    for (size_t i = 0; i < w->len; i++) free(w->items[i]);
    free(w->items);
    w->items = NULL;
    w->len = w->cap = 0;
}

static Words one_empty(void) {
    Words w = {0};
    push(&w, concat2("", ""));
    return w;
}

// every word of `words` followed by every word of `part`
static Words join(Words *words, Words *part) {
    Words out = {0};
    for (size_t i = 0; i < words->len; i++)
        for (size_t j = 0; j < part->len; j++) push(&out, concat2(words->items[i], part->items[j]));
    return out;
}

static void extend(Words *into, Words *from) {
    for (size_t i = 0; i < from->len; i++) push(into, from->items[i]);
    free(from->items);
    from->items = NULL;
    from->len = from->cap = 0;
}

static int cmp(const void *a, const void *b) { return strcmp(*(char *const *)a, *(char *const *)b); }

static void sort_dedup(Words *w) {
    qsort(w->items, w->len, sizeof(char *), cmp);
    size_t k = 0;
    for (size_t i = 0; i < w->len; i++) {
        if (k > 0 && strcmp(w->items[k - 1], w->items[i]) == 0) {
            free(w->items[i]);
        } else {
            w->items[k++] = w->items[i];
        }
    }
    w->len = k;
}

typedef struct {
    Words u, c;
} Frame;

static Words brace_expansion_ii(const char *expression) {
    Frame stack[64];
    int depth = 0;
    Words u = {0};
    Words c = one_empty();
    for (const char *p = expression; *p; p++) {
        if (*p == '{') {
            stack[depth].u = u;
            stack[depth].c = c;
            depth++;
            u = (Words){0};
            c = one_empty();
        } else if (*p == ',') {
            extend(&u, &c);
            c = one_empty();
        } else if (*p == '}') {
            extend(&u, &c);
            sort_dedup(&u);
            depth--;
            Words outer_u = stack[depth].u, outer_c = stack[depth].c;
            c = join(&outer_c, &u);
            release(&outer_c);
            release(&u);
            u = outer_u;
        } else {
            char letter[2] = {*p, 0};
            Words part = {0};
            push(&part, concat2(letter, ""));
            Words next = join(&c, &part);
            release(&part);
            release(&c);
            c = next;
        }
    }
    extend(&u, &c);
    sort_dedup(&u);
    return u;
}

static int64_t seed = 1096;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char letter(void) { return (char)('a' + next_random() % 6); }

// appends one option to s at *n
static void option(char *s, size_t *n) {
    if (next_random() % 4 == 0) {
        s[(*n)++] = '{';
        s[(*n)++] = letter();
        s[(*n)++] = ',';
        s[(*n)++] = letter();
        s[(*n)++] = '}';
        s[(*n)++] = letter();
    } else {
        int64_t k = next_random() % 2 + 1;
        for (int64_t i = 0; i < k; i++) s[(*n)++] = letter();
    }
}

int main(void) {
    char expressions[64][64];
    int count = 0;
    while (count < 64) {
        char s[256];
        size_t n = 0;
        for (int p = 0; p < 5; p++) {
            s[n++] = '{';
            int64_t k = next_random() % 2 + 2;
            for (int64_t i = 0; i < k; i++) {
                if (i > 0) s[n++] = ',';
                option(s, &n);
            }
            s[n++] = '}';
        }
        s[n] = 0;
        if (n <= 60) {
            memcpy(expressions[count], s, n + 1);
            count++;
        }
    }
    int64_t total = 0, check = 0;
    for (int64_t round = 0; round < 200; round++) {
        for (int64_t j = 0; j < 64; j++) {
            char *e = expressions[j];
            int64_t len = (int64_t)strlen(e);
            int64_t at = (round * 7 + j * 13) % len;
            if (e[at] >= 'a' && e[at] <= 'z') e[at] = (char)('a' + (round + j) % 6);
            Words words = brace_expansion_ii(e);
            total += (int64_t)words.len;
            check = (check * 31 + (int64_t)words.len) % 1000000007;
            for (const char *b = words.items[0]; *b; b++) check = (check * 131 + (unsigned char)*b) % 1000000007;
            for (const char *b = words.items[words.len - 1]; *b; b++)
                check = (check * 131 + (unsigned char)*b) % 1000000007;
            release(&words);
        }
    }
    printf("200 rounds over 64 expressions: %lld words, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
