// LeetCode #1597: Build Binary Expression Tree From Infix Expression
// -- the bench in C, mirroring expression_tree.kara: two stacks, as the
// shunting-yard reads an expression, each node a malloc freed with its
// tree, on 200000 expressions of up to 50 digits, all drawn first, each
// tree folded to a hash. Each expression is a malloc'd string, as Kāra's
// String is.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    char val;
    struct Node *left, *right;
} Node;

static Node *node(char val, Node *left, Node *right) {
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

static int precedence(char op) {
    return op == '+' || op == '-' ? 1 : op == '*' || op == '/' ? 2 : 0;
}

typedef struct {
    char ops[256];
    int nops;
    Node *trees[256];
    int ntrees;
} Stacks;

static void join(Stacks *st) {
    char op = st->ops[--st->nops];
    Node *right = st->trees[--st->ntrees];
    Node *left = st->trees[--st->ntrees];
    st->trees[st->ntrees++] = node(op, left, right);
}

static Node *exp_tree(const char *s) {
    Stacks st;
    st.nops = 0;
    st.ntrees = 0;
    for (; *s; s++) {
        char c = *s;
        if (c >= '0' && c <= '9') {
            st.trees[st.ntrees++] = node(c, NULL, NULL);
        } else if (c == '(') {
            st.ops[st.nops++] = c;
        } else if (c == ')') {
            while (st.ops[st.nops - 1] != '(') join(&st);
            st.nops--;
        } else {
            while (st.nops > 0 && precedence(st.ops[st.nops - 1]) >= precedence(c)) join(&st);
            st.ops[st.nops++] = c;
        }
    }
    while (st.nops > 0) join(&st);
    return st.trees[--st.ntrees];
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

// Appends a random expression to buf at *len.
static void expression(int64_t operands, int64_t *seed, char *buf, int *len) {
    if (operands <= 1 || next_random(seed) % 4 == 0) {
        buf[(*len)++] = (char)('0' + next_random(seed) % 10);
        return;
    }
    int64_t left = next_random(seed) % (operands - 1) + 1;
    char op = "+-*/"[next_random(seed) % 4];
    int start = *len;
    expression(left, seed, buf, len);
    buf[(*len)++] = op;
    expression(operands - left, seed, buf, len);
    if (next_random(seed) % 4 == 0) {
        memmove(buf + start + 1, buf + start, *len - start);
        buf[start] = '(';
        (*len)++;
        buf[(*len)++] = ')';
    }
}

static int64_t fold(Node *n) {
    int64_t left = n->left ? fold(n->left) : 7;
    int64_t right = n->right ? fold(n->right) : 11;
    return ((int64_t)n->val * 1000003 + left * 31 + right * 17) % 1000000007;
}

int main(void) {
    enum { N = 200000 };
    int64_t seed = 1597;
    char **texts = malloc(sizeof(char *) * N);
    char buf[1024];
    for (int i = 0; i < N; i++) {
        int64_t operands = next_random(&seed) % 50 + 1;
        int len = 0;
        expression(operands, &seed, buf, &len);
        texts[i] = malloc(len + 1);
        memcpy(texts[i], buf, len);
        texts[i][len] = 0;
    }
    int64_t check = 0, length = 0;
    for (int i = 0; i < N; i++) {
        length += strlen(texts[i]);
        Node *tree = exp_tree(texts[i]);
        check = (check * 31 + fold(tree)) % 1000000007;
        drop(tree);
    }
    printf("200000 expressions, %lld characters: checksum %lld\n", (long long)length, (long long)check);
    for (int i = 0; i < N; i++) free(texts[i]);
    free(texts);
    return 0;
}
