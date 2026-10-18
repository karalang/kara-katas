// LeetCode #736: Parse Lisp Expression -- tokens, recursion and a stack
// of scopes.
// Benchmark mirror of the Kara star arm: split the text into tokens,
// then evaluate by recursion, keeping the assignments of each open let
// in a scope of its own and looking a name up from the innermost. As C
// would, a token is a pointer and a length into the text rather than a
// copy, and each scope is a short array searched in turn rather than a
// hash map; the Kara, Rust, Go and Python programs copy the tokens and
// give each scope a hash map.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    const char *s;
    int len;
} Tok;

typedef struct {
    const char *name;
    int len;
    int64_t value;
} Binding;

typedef struct {
    Binding *b;
    int len, cap;
} Scope;

static Tok *tokens;
static int ntokens, captokens;
static Scope *scopes;
static int nscopes, capscopes;

static void push_token(const char *s, int len) {
    if (ntokens == captokens) {
        captokens = captokens ? captokens * 2 : 64;
        tokens = realloc(tokens, captokens * sizeof(Tok));
    }
    tokens[ntokens].s = s;
    tokens[ntokens].len = len;
    ntokens++;
}

static void tokenize(const char *e) {
    ntokens = 0;
    int start = -1;
    for (int i = 0; e[i]; i++) {
        char c = e[i];
        if (c == '(' || c == ')' || c == ' ') {
            if (start >= 0) {
                push_token(e + start, i - start);
                start = -1;
            }
            if (c != ' ') push_token(e + i, 1);
        } else if (start < 0) {
            start = i;
        }
    }
    if (start >= 0) push_token(e + start, (int)strlen(e) - start);
}

static int tok_is(Tok t, const char *s) { return t.len == (int)strlen(s) && memcmp(t.s, s, t.len) == 0; }

static int64_t lookup(Tok t) {
    for (int i = nscopes - 1; i >= 0; i--) {
        Scope *sc = &scopes[i];
        for (int k = 0; k < sc->len; k++)
            if (sc->b[k].len == t.len && memcmp(sc->b[k].name, t.s, t.len) == 0) return sc->b[k].value;
    }
    return 0;
}

static void assign(Tok name, int64_t v) {
    Scope *sc = &scopes[nscopes - 1];
    for (int k = 0; k < sc->len; k++)
        if (sc->b[k].len == name.len && memcmp(sc->b[k].name, name.s, name.len) == 0) {
            sc->b[k].value = v;
            return;
        }
    if (sc->len == sc->cap) {
        sc->cap = sc->cap ? sc->cap * 2 : 4;
        sc->b = realloc(sc->b, sc->cap * sizeof(Binding));
    }
    sc->b[sc->len++] = (Binding){name.s, name.len, v};
}

static int64_t eval(int *pos) {
    Tok t = tokens[(*pos)++];
    if (!tok_is(t, "(")) {
        if (t.s[0] == '-' || (t.s[0] >= '0' && t.s[0] <= '9')) {
            int64_t sign = 1, n = 0;
            int i = 0;
            if (t.s[0] == '-') sign = -1, i = 1;
            for (; i < t.len; i++) n = n * 10 + (t.s[i] - '0');
            return sign * n;
        }
        return lookup(t);
    }
    Tok op = tokens[(*pos)++];
    int64_t value;
    if (tok_is(op, "add")) {
        int64_t a = eval(pos);
        int64_t b = eval(pos);
        value = a + b;
    } else if (tok_is(op, "mult")) {
        int64_t a = eval(pos);
        int64_t b = eval(pos);
        value = a * b;
    } else {
        if (nscopes == capscopes) {
            capscopes = capscopes ? capscopes * 2 : 16;
            scopes = realloc(scopes, capscopes * sizeof(Scope));
        }
        scopes[nscopes++] = (Scope){0, 0, 0};
        for (;;) {
            Tok name = tokens[*pos];
            if (!tok_is(name, "(") && !tok_is(tokens[*pos + 1], ")")) {
                (*pos)++;
                int64_t v = eval(pos);
                assign(name, v);
            } else {
                value = eval(pos);
                break;
            }
        }
        free(scopes[--nscopes].b);
    }
    (*pos)++;
    return value;
}

static int64_t evaluate(const char *e) {
    tokenize(e);
    int pos = 0;
    return eval(&pos);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static char *fmt(const char *f, ...) __attribute__((format(printf, 1, 2)));
#include <stdarg.h>
static char *fmt(const char *f, ...) {
    va_list ap, aq;
    va_start(ap, f);
    va_copy(aq, ap);
    int n = vsnprintf(NULL, 0, f, ap);
    va_end(ap);
    char *s = malloc(n + 1);
    vsnprintf(s, n + 1, f, aq);
    va_end(aq);
    return s;
}

static const char *pool[] = {"x", "y", "z", "a1", "b2"};

static char *random_expr(int64_t *seed, int64_t depth, const char **names, int nnames) {
    int64_t kinds = depth == 0 ? 2 : 5;
    int64_t kind = next_random(seed) % kinds;
    if (kind == 0 || (kind == 1 && nnames == 0)) return fmt("%lld", (long long)(next_random(seed) % 21 - 10));
    if (kind == 1) return fmt("%s", names[next_random(seed) % nnames]);
    if (kind == 2) {
        char *a = random_expr(seed, depth - 1, names, nnames);
        char *b = random_expr(seed, depth - 1, names, nnames);
        char *s = fmt("(add %s %s)", a, b);
        free(a);
        free(b);
        return s;
    }
    if (kind == 3) {
        char *a = random_expr(seed, depth - 1, names, nnames);
        char *s = fmt("(mult %s %lld)", a, (long long)(next_random(seed) % 5 - 2));
        free(a);
        return s;
    }
    const char *inner[8];
    int ninner = nnames;
    memcpy(inner, names, nnames * sizeof(char *));
    char *text = fmt("(let");
    int64_t count = 1 + next_random(seed) % 3;
    for (int64_t k = 0; k < count; k++) {
        const char *name = pool[next_random(seed) % 5];
        char *v = random_expr(seed, depth - 1, inner, ninner);
        char *t = fmt("%s %s %s", text, name, v);
        free(text);
        free(v);
        text = t;
        int found = 0;
        for (int i = 0; i < ninner; i++)
            if (strcmp(inner[i], name) == 0) found = 1;
        if (!found) inner[ninner++] = name;
    }
    char *body = random_expr(seed, depth - 1, inner, ninner);
    char *s = fmt("%s %s)", text, body);
    free(text);
    free(body);
    return s;
}

int main(void) {
    int64_t seed = 736;
    char *exprs[1000];
    int n = 0;
    long long chars = 0;
    while (n < 1000) {
        char *e = random_expr(&seed, 8, NULL, 0);
        size_t len = strlen(e);
        if (len >= 500 && len <= 2000) {
            chars += len;
            exprs[n++] = e;
        } else {
            free(e);
        }
    }
    int64_t sum = 0;
    for (int r = 0; r < 40; r++)
        for (int i = 0; i < 1000; i++) {
            int64_t v = evaluate(exprs[i]);
            sum = (sum * 31 + (v % 1000000007 + 1000000007) % 1000000007) % 1000000007;
        }
    printf("40 rounds of 1000 expressions of %lld characters in all: checksum %lld\n", chars, (long long)sum);
    for (int i = 0; i < 1000; i++) free(exprs[i]);
    free(tokens);
    free(scopes);
    return 0;
}
