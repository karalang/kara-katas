// Benchmark for #536: C mirror of the ★ arm (recursive descent); see
// str2tree.kara. Nodes are malloc'd one at a time and the whole tree is
// freed after each read, as the ★ arm's tree is dropped.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    int64_t val;
    struct Node *left, *right;
} Node;

static Node *node(int64_t val, Node *left, Node *right) {
    Node *n = malloc(sizeof(Node));
    n->val = val;
    n->left = left;
    n->right = right;
    return n;
}

static void drop(Node *n) {
    if (!n) return;
    drop(n->left);
    drop(n->right);
    free(n);
}

// The tree that starts at byte *i, leaving *i just past it.
static Node *parse(const char *b, int64_t len, int64_t *i) {
    int64_t sign = 1;
    if (b[*i] == '-') {
        sign = -1;
        (*i)++;
    }
    int64_t val = 0;
    while (*i < len && b[*i] >= '0' && b[*i] <= '9') {
        val = val * 10 + (b[*i] - '0');
        (*i)++;
    }
    Node *n = node(sign * val, NULL, NULL);
    if (*i < len && b[*i] == '(') {
        (*i)++;
        n->left = parse(b, len, i);
        (*i)++;
    }
    if (*i < len && b[*i] == '(') {
        (*i)++;
        n->right = parse(b, len, i);
        (*i)++;
    }
    return n;
}

static Node *str2tree(const char *s, int64_t len) {
    if (len == 0) return NULL;
    int64_t i = 0;
    return parse(s, len, &i);
}

static int64_t seed = 536;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static Node *random_tree(int64_t n) {
    if (n == 0) return NULL;
    int64_t val = next_random() % 2001 - 1000;
    int64_t rest = n - 1;
    int64_t left;
    if (rest == 0) left = 0;
    else if (next_random() % 3 == 0) left = rest;
    else left = 1 + next_random() % rest;
    Node *l = random_tree(left);
    Node *r = random_tree(rest - left);
    return node(val, l, r);
}

typedef struct {
    char *s;
    int64_t len, cap;
} Buf;

static void put(Buf *b, const char *s, int64_t n) {
    if (b->len + n > b->cap) {
        while (b->len + n > b->cap) b->cap = b->cap ? 2 * b->cap : 64;
        b->s = realloc(b->s, b->cap);
    }
    memcpy(b->s + b->len, s, n);
    b->len += n;
}

static void render(const Node *n, Buf *out) {
    if (!n) return;
    char num[24];
    int k = snprintf(num, sizeof num, "%lld", (long long)n->val);
    put(out, num, k);
    if (n->left) {
        put(out, "(", 1);
        render(n->left, out);
        put(out, ")", 1);
    }
    if (n->right) {
        put(out, "(", 1);
        render(n->right, out);
        put(out, ")", 1);
    }
}

static void walk(const Node *n, int64_t *stats) {
    if (!n) return;
    stats[0]++;
    stats[1] = (stats[1] * 31 + n->val + 1000) % 1000000007;
    walk(n->left, stats);
    walk(n->right, stats);
}

int main(void) {
    Buf strings[20];
    for (int k = 0; k < 20; k++) {
        Node *tree = random_tree(5500);
        strings[k] = (Buf){NULL, 0, 0};
        render(tree, &strings[k]);
        drop(tree);
    }
    int64_t rounds = 100;
    int64_t stats[2] = {0, 0};
    for (int64_t r = 0; r < rounds; r++) {
        for (int k = 0; k < 20; k++) {
            Node *t = str2tree(strings[k].s, strings[k].len);
            walk(t, stats);
            drop(t);
        }
    }
    printf("20 strings, %lld rounds: %lld nodes, checksum %lld\n", (long long)rounds, (long long)stats[0], (long long)stats[1]);
    for (int k = 0; k < 20; k++) free(strings[k].s);
    return 0;
}
