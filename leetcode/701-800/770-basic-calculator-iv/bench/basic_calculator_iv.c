// LeetCode 770 — Basic Calculator IV: benchmark, the ★ arm in C.
// Sixty-four random expressions of 40 leaves, built once; 20,000 rounds
// each simplify the next of them. A polynomial is an open-addressing
// hash map from a term's sorted, '*'-joined variables to its coefficient.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <ctype.h>

typedef struct {
    char **keys;
    int64_t *coefs;
    int cap, len;
} Poly;

static uint64_t hash(const char *s) {
    uint64_t h = 1469598103934665603ULL;
    for (; *s; s++) h = (h ^ (unsigned char)*s) * 1099511628211ULL;
    return h;
}

static void poly_init(Poly *p) {
    p->cap = 8;
    p->len = 0;
    p->keys = calloc(p->cap, sizeof(char *));
    p->coefs = calloc(p->cap, sizeof(int64_t));
}

static void poly_free(Poly *p) {
    for (int i = 0; i < p->cap; i++) free(p->keys[i]);
    free(p->keys);
    free(p->coefs);
}

static void poly_add(Poly *p, const char *key, int64_t delta);

static void poly_grow(Poly *p) {
    Poly bigger;
    bigger.cap = p->cap * 2;
    bigger.len = 0;
    bigger.keys = calloc(bigger.cap, sizeof(char *));
    bigger.coefs = calloc(bigger.cap, sizeof(int64_t));
    for (int i = 0; i < p->cap; i++)
        if (p->keys[i]) poly_add(&bigger, p->keys[i], p->coefs[i]);
    poly_free(p);
    *p = bigger;
}

// Adds `delta` to the coefficient of `key`, inserting it if absent.
static void poly_add(Poly *p, const char *key, int64_t delta) {
    if (2 * (p->len + 1) > p->cap) poly_grow(p);
    uint64_t i = hash(key) & (p->cap - 1);
    while (p->keys[i] && strcmp(p->keys[i], key) != 0) i = (i + 1) & (p->cap - 1);
    if (!p->keys[i]) {
        p->keys[i] = strdup(key);
        p->len++;
    }
    p->coefs[i] += delta;
}

static int cmp_str(const void *a, const void *b) {
    return strcmp(*(char *const *)a, *(char *const *)b);
}

// Splits a non-empty key on '*' into `names`, returning how many.
static int split_names(const char *key, char names[][16], int n) {
    if (!*key) return n;
    const char *start = key;
    for (const char *c = key;; c++) {
        if (*c == '*' || *c == 0) {
            memcpy(names[n], start, c - start);
            names[n][c - start] = 0;
            n++;
            if (*c == 0) break;
            start = c + 1;
        }
    }
    return n;
}

static int degree_of(const char *key) {
    if (!*key) return 0;
    int d = 1;
    for (; *key; key++) d += *key == '*';
    return d;
}

static Poly multiply(Poly *a, Poly *b) {
    Poly product;
    poly_init(&product);
    static char names[64][16];
    char *order[64];
    char key[1024];
    for (int i = 0; i < a->cap; i++) {
        if (!a->keys[i]) continue;
        for (int j = 0; j < b->cap; j++) {
            if (!b->keys[j]) continue;
            int n = split_names(a->keys[i], names, 0);
            n = split_names(b->keys[j], names, n);
            for (int k = 0; k < n; k++) order[k] = names[k];
            qsort(order, n, sizeof(char *), cmp_str);
            key[0] = 0;
            size_t len = 0;
            for (int k = 0; k < n; k++) {
                if (k > 0) key[len++] = '*';
                size_t m = strlen(order[k]);
                memcpy(key + len, order[k], m);
                len += m;
            }
            key[len] = 0;
            poly_add(&product, key, a->coefs[i] * b->coefs[j]);
        }
    }
    return product;
}

typedef struct {
    char **tokens;
    int count, at;
    const char *known_name;
    int64_t known_value;
} Reader;

static const char *peek(Reader *r) { return r->at < r->count ? r->tokens[r->at] : ""; }

static Poly expression(Reader *r);

static Poly factor(Reader *r) {
    const char *token = peek(r);
    r->at++;
    Poly p;
    if (strcmp(token, "(") == 0) {
        p = expression(r);
        r->at++;
    } else {
        poly_init(&p);
        if (isdigit((unsigned char)token[0]))
            poly_add(&p, "", strtoll(token, NULL, 10));
        else if (r->known_name && strcmp(token, r->known_name) == 0)
            poly_add(&p, "", r->known_value);
        else
            poly_add(&p, token, 1);
    }
    return p;
}

static Poly term(Reader *r) {
    Poly product = factor(r);
    while (strcmp(peek(r), "*") == 0) {
        r->at++;
        Poly next = factor(r);
        Poly m = multiply(&product, &next);
        poly_free(&product);
        poly_free(&next);
        product = m;
    }
    return product;
}

static Poly expression(Reader *r) {
    Poly total = term(r);
    while (strcmp(peek(r), "+") == 0 || strcmp(peek(r), "-") == 0) {
        int64_t sign = strcmp(peek(r), "+") == 0 ? 1 : -1;
        r->at++;
        Poly next = term(r);
        for (int i = 0; i < next.cap; i++)
            if (next.keys[i]) poly_add(&total, next.keys[i], sign * next.coefs[i]);
        poly_free(&next);
    }
    return total;
}

typedef struct {
    int degree;
    char *key;
    int64_t coef;
} Term;

static int cmp_term(const void *a, const void *b) {
    const Term *x = a, *y = b;
    if (x->degree != y->degree) return x->degree < y->degree ? -1 : 1;
    return strcmp(x->key, y->key);
}

// Writes the answer's terms into `answer`, returning how many.
static int basic_calculator_iv(const char *e, const char *name, int64_t value, char answer[][256]) {
    char *tokens[512];
    int count = 0;
    char word[64];
    int wl = 0;
    for (const char *c = e;; c++) {
        if (*c && isalnum((unsigned char)*c)) {
            word[wl++] = *c;
        } else {
            if (wl > 0) {
                word[wl] = 0;
                tokens[count++] = strdup(word);
                wl = 0;
            }
            if (!*c) break;
            if (*c != ' ') {
                char one[2] = {*c, 0};
                tokens[count++] = strdup(one);
            }
        }
    }
    Reader r = {tokens, count, 0, name, value};
    Poly p = expression(&r);
    Term *terms = malloc(p.cap * sizeof(Term));
    int n = 0;
    for (int i = 0; i < p.cap; i++)
        if (p.keys[i] && p.coefs[i] != 0)
            terms[n++] = (Term){-degree_of(p.keys[i]), p.keys[i], p.coefs[i]};
    qsort(terms, n, sizeof(Term), cmp_term);
    for (int i = 0; i < n; i++) {
        if (!*terms[i].key)
            snprintf(answer[i], 256, "%lld", (long long)terms[i].coef);
        else
            snprintf(answer[i], 256, "%lld*%s", (long long)terms[i].coef, terms[i].key);
    }
    free(terms);
    poly_free(&p);
    for (int i = 0; i < count; i++) free(tokens[i]);
    return n;
}

static int64_t seed = 770;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char *random_expression(int64_t size) {
    char *out = malloc(1024);
    if (size <= 1) {
        int64_t pick = next_random() % 9;
        if (pick < 3)
            snprintf(out, 1024, "%lld", (long long)(next_random() % 10));
        else
            snprintf(out, 1024, "%s", (const char *[]){"a", "b", "c", "d", "x", "y"}[pick - 3]);
        return out;
    }
    int64_t left = 1 + next_random() % (size - 1);
    char *a = random_expression(left);
    char *b = random_expression(size - left);
    const char *op = (const char *[]){" + ", " - ", " * "}[next_random() % 3];
    if (next_random() % 3 == 0)
        snprintf(out, 1024, "(%s%s%s)", a, op, b);
    else
        snprintf(out, 1024, "%s%s%s", a, op, b);
    free(a);
    free(b);
    return out;
}

int main(void) {
    int64_t rounds = 20000;
    char *pool[64];
    size_t longest = 0;
    for (int i = 0; i < 64; i++) {
        pool[i] = random_expression(40);
        if (strlen(pool[i]) > longest) longest = strlen(pool[i]);
    }
    static char answer[4096][256];
    int64_t terms = 0, check = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int n = basic_calculator_iv(pool[round % 64], "x", round % 7 - 3, answer);
        terms += n;
        for (int i = 0; i < n; i++)
            for (const char *c = answer[i]; *c; c++) check = (check * 31 + (unsigned char)*c) % 1000000007;
    }
    printf("%lld expressions of up to %zu characters: %lld terms in all, checksum %lld\n",
           (long long)rounds, longest, (long long)terms, (long long)check);
    return 0;
}
