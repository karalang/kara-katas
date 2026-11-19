// LeetCode #1628: Design an Expression Tree With Evaluate Function -- the
// bench's C mirror: a node is a pointer to a table of its methods, one
// table per operator, as a trait object is; 20000 random postfix
// expressions of 50 operands, all drawn first, each built into a tree of
// heap nodes, evaluated, and freed.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node Node;
typedef struct {
    int64_t (*evaluate)(const Node *);
} NodeTable;

struct Node {
    const NodeTable *table;
    int64_t value;
    Node *left, *right;
};

static int64_t eval(const Node *n) { return n->table->evaluate(n); }
static int64_t number_eval(const Node *n) { return n->value; }
static int64_t add_eval(const Node *n) { return eval(n->left) + eval(n->right); }
static int64_t subtract_eval(const Node *n) { return eval(n->left) - eval(n->right); }
static int64_t multiply_eval(const Node *n) { return eval(n->left) * eval(n->right); }
static int64_t divide_eval(const Node *n) { return eval(n->left) / eval(n->right); }

static const NodeTable NUMBER = {number_eval}, ADD = {add_eval}, SUBTRACT = {subtract_eval},
                       MULTIPLY = {multiply_eval}, DIVIDE = {divide_eval};

static Node *node(const NodeTable *table, int64_t value, Node *left, Node *right) {
    Node *n = malloc(sizeof(Node));
    n->table = table;
    n->value = value;
    n->left = left;
    n->right = right;
    return n;
}

static void free_tree(Node *n) {
    if (!n) return;
    free_tree(n->left);
    free_tree(n->right);
    free(n);
}

static Node *build_tree(char **postfix, int count) {
    Node **stack = malloc(sizeof(Node *) * (size_t)count);
    int top = 0;
    for (int i = 0; i < count; i++) {
        const char *token = postfix[i];
        if (token[0] >= '0' && token[0] <= '9') {
            stack[top++] = node(&NUMBER, strtoll(token, NULL, 10), NULL, NULL);
        } else {
            Node *right = stack[--top];
            Node *left = stack[--top];
            const NodeTable *t = token[0] == '+' ? &ADD : token[0] == '-' ? &SUBTRACT : token[0] == '*' ? &MULTIPLY : &DIVIDE;
            stack[top++] = node(t, 0, left, right);
        }
    }
    Node *root = stack[0];
    free(stack);
    return root;
}

static int64_t seed = 1628;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct {
    char **tokens;
    int count;
} Postfix;

static void push(Postfix *p, const char *s) {
    p->tokens[p->count] = malloc(strlen(s) + 1);
    strcpy(p->tokens[p->count++], s);
}

static int64_t expression(int64_t leaves, int64_t top, Postfix *tokens) {
    if (leaves == 1) {
        int64_t v = next_random() % top;
        char buf[24];
        snprintf(buf, sizeof buf, "%lld", (long long)v);
        push(tokens, buf);
        return v;
    }
    int64_t left = next_random() % (leaves - 1) + 1;
    int64_t a = expression(left, top, tokens);
    int64_t b = expression(leaves - left, top, tokens);
    char op = "+-*/"[next_random() % 4];
    if (op == '/' && b == 0) op = '*';
    if (op == '*' && llabs(a * b) > 1000000000) op = '+';
    if (op == '+' && llabs(a + b) > 1000000000) op = '-';
    if (op == '-' && llabs(a - b) > 1000000000) op = '+';
    char s[2] = {op, 0};
    push(tokens, s);
    switch (op) {
    case '+': return a + b;
    case '-': return a - b;
    case '*': return a * b;
    default: return a / b;
    }
}

int main(void) {
    enum { COUNT = 20000, OPERANDS = 50 };
    static Postfix expressions[COUNT];
    for (int i = 0; i < COUNT; i++) {
        expressions[i].tokens = malloc(sizeof(char *) * (2 * OPERANDS - 1));
        expressions[i].count = 0;
        expression(OPERANDS, 100001, &expressions[i]);
    }
    int64_t check = 0, total = 0;
    for (int i = 0; i < COUNT; i++) {
        Node *tree = build_tree(expressions[i].tokens, expressions[i].count);
        int64_t got = eval(tree);
        free_tree(tree);
        total += got;
        check = ((check * 31 + got + 1) % 1000000007 + 1000000007) % 1000000007;
    }
    for (int i = 0; i < COUNT; i++) {
        for (int j = 0; j < expressions[i].count; j++) free(expressions[i].tokens[j]);
        free(expressions[i].tokens);
    }
    printf("20000 expressions of 50 operands: values sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
