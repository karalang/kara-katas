/* LeetCode 297 benchmark lane — C mirror of treecodec.kara.
 *
 * Same algorithm, same tree shape, same sink: build one balanced 200k-node
 * tree, then 24 chained serialize/deserialize round trips, hashing every
 * encoded string. See the .kara file's header for the workload rationale. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    long long val;
    struct Node *left, *right;
} Node;

static Node *build(const long long *vals, long lo, long hi) {
    if (lo >= hi) return NULL;
    long mid = lo + (hi - lo) / 2;
    Node *n = (Node *)malloc(sizeof(Node));
    n->val = vals[mid];
    n->left = build(vals, lo, mid);
    n->right = build(vals, mid + 1, hi);
    return n;
}

static void free_tree(Node *t) {
    if (!t) return;
    free_tree(t->left);
    free_tree(t->right);
    free(t);
}

/* Serialize into a growable buffer, comma-separated, `#` for an empty slot. */
typedef struct { char *p; size_t len, cap; } Buf;

static void buf_reserve(Buf *b, size_t extra) {
    if (b->len + extra + 1 <= b->cap) return;
    while (b->len + extra + 1 > b->cap) b->cap = b->cap ? b->cap * 2 : 4096;
    b->p = (char *)realloc(b->p, b->cap);
}

static void ser_into(const Node *t, Buf *b) {
    if (b->len) { buf_reserve(b, 1); b->p[b->len++] = ','; }
    if (!t) { buf_reserve(b, 1); b->p[b->len++] = '#'; return; }
    char tmp[24];
    int k = snprintf(tmp, sizeof tmp, "%lld", t->val);
    buf_reserve(b, (size_t)k);
    memcpy(b->p + b->len, tmp, (size_t)k);
    b->len += (size_t)k;
    ser_into(t->left, b);
    ser_into(t->right, b);
}

static char *serialize(const Node *t, size_t *out_len) {
    Buf b = {NULL, 0, 0};
    ser_into(t, &b);
    buf_reserve(&b, 0);
    b.p[b.len] = '\0';
    *out_len = b.len;
    return b.p;
}

/* Deserialize with one moving cursor over the comma-separated tokens. */
static Node *de_at(char **toks, long *i) {
    const char *tok = toks[(*i)++];
    if (tok[0] == '#' && tok[1] == '\0') return NULL;
    Node *n = (Node *)malloc(sizeof(Node));
    n->val = strtoll(tok, NULL, 10);
    n->left = de_at(toks, i);
    n->right = de_at(toks, i);
    return n;
}

static Node *deserialize(char *s, size_t len) {
    /* Split in place: count commas, then replace each with NUL. */
    long ntok = 1;
    for (size_t k = 0; k < len; k++) if (s[k] == ',') ntok++;
    char **toks = (char **)malloc((size_t)ntok * sizeof(char *));
    long t = 0;
    toks[t++] = s;
    for (size_t k = 0; k < len; k++) {
        if (s[k] == ',') { s[k] = '\0'; toks[t++] = s + k + 1; }
    }
    long i = 0;
    Node *root = de_at(toks, &i);
    free(toks);
    return root;
}

static long long hash_string(const char *s, size_t len, long long seed) {
    long long h = seed;
    for (size_t k = 0; k < len; k++)
        h = (h * 131 + (long long)(unsigned char)s[k]) % 1000000007LL;
    return h;
}

int main(void) {
    const long n = 200000;
    const int rounds = 24;

    long long *vals = (long long *)malloc((size_t)n * sizeof(long long));
    long long state = 12345;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245LL + 12345LL) & 0x7fffffffLL;
        vals[i] = state % 1000003LL - 500000LL;
    }

    Node *tree = build(vals, 0, n);
    long long checksum = 0;

    for (int r = 0; r < rounds; r++) {
        size_t len;
        char *s = serialize(tree, &len);
        checksum = hash_string(s, len, checksum);
        free_tree(tree);
        tree = deserialize(s, len);
        free(s);
    }

    printf("nodes %ld rounds %d checksum %lld\n", n, rounds, checksum);
    free_tree(tree);
    free(vals);
    return 0;
}
