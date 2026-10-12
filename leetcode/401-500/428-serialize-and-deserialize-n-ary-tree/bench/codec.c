// Benchmark for #428: mirror of codec.kara (preorder with child
// counts). Each word of the text is copied out on its own, as the Kāra
// program's split makes a String of each; trees and words are freed
// every round.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    int64_t val;
    struct Node **children;
    int64_t len, cap;
} Node;

static Node *new_node(int64_t val) {
    Node *n = malloc(sizeof *n);
    n->val = val;
    n->children = NULL;
    n->len = n->cap = 0;
    return n;
}

static void add_child(Node *n, Node *child) {
    if (n->len == n->cap) {
        n->cap = n->cap ? n->cap * 2 : 4;
        n->children = realloc(n->children, n->cap * sizeof *n->children);
    }
    n->children[n->len++] = child;
}

static void free_tree(Node *n) {
    for (int64_t i = 0; i < n->len; i++) free_tree(n->children[i]);
    free(n->children);
    free(n);
}

typedef struct { char *buf; int64_t len, cap; } Text;

static void append(Text *t, const char *s, int64_t k) {
    while (t->len + k + 1 > t->cap) {
        t->cap = t->cap ? t->cap * 2 : 64;
        t->buf = realloc(t->buf, t->cap);
    }
    memcpy(t->buf + t->len, s, k);
    t->len += k;
    t->buf[t->len] = 0;
}

static void write_node(Node *node, Text *out) {
    char tmp[48];
    int k = snprintf(tmp, sizeof tmp, "%s%lld %lld", out->len > 0 ? " " : "", (long long)node->val, (long long)node->len);
    append(out, tmp, k);
    for (int64_t i = 0; i < node->len; i++) write_node(node->children[i], out);
}

static Text serialize(Node *root) {
    Text out = {0};
    append(&out, "", 0);
    if (root) write_node(root, &out);
    return out;
}

static Node *read_node(char **words, int64_t *at) {
    int64_t val = atoll(words[*at]);
    int64_t count = atoll(words[*at + 1]);
    *at += 2;
    Node *n = new_node(val);
    for (int64_t i = 0; i < count; i++) add_child(n, read_node(words, at));
    return n;
}

static Node *deserialize(const char *data, int64_t len) {
    if (len == 0) return NULL;
    int64_t cap = 64, count = 0;
    char **words = malloc(cap * sizeof *words);
    int64_t start = 0;
    for (int64_t i = 0; i <= len; i++) {
        if (i == len || data[i] == ' ') {
            if (count == cap) {
                cap *= 2;
                words = realloc(words, cap * sizeof *words);
            }
            char *w = malloc(i - start + 1);
            memcpy(w, data + start, i - start);
            w[i - start] = 0;
            words[count++] = w;
            start = i + 1;
        }
    }
    int64_t at = 0;
    Node *root = read_node(words, &at);
    for (int64_t i = 0; i < count; i++) free(words[i]);
    free(words);
    return root;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t total(Node *n) {
    int64_t sum = n->val;
    for (int64_t i = 0; i < n->len; i++) sum += total(n->children[i]);
    return sum;
}

typedef struct { int64_t *items; int64_t len, cap; } List;

static void push(List *l, int64_t v) {
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->items = realloc(l->items, l->cap * sizeof *l->items);
    }
    l->items[l->len++] = v;
}

static Node *build_random(int64_t i, int64_t *vals, List *kids) {
    Node *n = new_node(vals[i]);
    for (int64_t j = 0; j < kids[i].len; j++) add_child(n, build_random(kids[i].items[j], vals, kids));
    return n;
}

int main(int argc, char **argv) {
    int64_t n = 10000;
    int64_t rounds = argc > 1 ? atoll(argv[1]) : 100;
    int64_t seed = 428;
    int64_t chars = 0, checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t reach = 1 + step(&seed) % 1000;
        int64_t *vals = malloc(n * sizeof *vals);
        List *kids = calloc(n, sizeof *kids);
        for (int64_t i = 0; i < n; i++) {
            vals[i] = step(&seed) % 10001;
            if (i > 0) {
                int64_t lim = i < reach ? i : reach;
                int64_t back = 1 + step(&seed) % lim;
                push(&kids[i - back], i);
            }
        }
        Node *tree = build_random(0, vals, kids);
        Text text = serialize(tree);
        Node *back = deserialize(text.buf, text.len);
        chars += text.len;
        checksum = (checksum * 31 + text.len + total(back)) % 1000000007;
        free_tree(back);
        free_tree(tree);
        free(text.buf);
        for (int64_t i = 0; i < n; i++) free(kids[i].items);
        free(kids);
        free(vals);
    }
    printf("%lld rounds of %lld nodes: %lld characters, checksum %lld\n", (long long)rounds, (long long)n, (long long)chars, (long long)checksum);
    return 0;
}
