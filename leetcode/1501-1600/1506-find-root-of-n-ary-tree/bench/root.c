// LeetCode #1506: Find Root of N-Ary Tree -- the benchmark, the same
// algorithm as root.kara: all values less all children's values. The
// nodes live as long as the program, so C keeps plain pointers; the list
// handed to each search is a fresh copy, as the other languages' are.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    int64_t val;
    struct Node **children;
    int64_t nchildren;
} Node;

static Node *find_root(Node **nodes, int64_t n) {
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        total += nodes[i]->val;
        for (int64_t c = 0; c < nodes[i]->nchildren; c++) total -= nodes[i]->children[c]->val;
    }
    for (int64_t i = 0; i < n; i++)
        if (nodes[i]->val == total) return nodes[i];
    return nodes[0];
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

static Node **random_tree(int64_t most, int64_t *seed, int64_t *len) {
    int64_t n = next_random(seed) % most + 1;
    int64_t *vals = malloc(n * sizeof(int64_t));
    char *seen = calloc(50001, 1);
    int64_t count = 0;
    while (count < n) {
        int64_t a = next_random(seed);
        int64_t v = (a * 65536 + next_random(seed)) % 50001;
        if (!seen[v]) { seen[v] = 1; vals[count++] = v; }
    }
    int64_t *parent = malloc(n * sizeof(int64_t));
    int64_t *nkids = calloc(n, sizeof(int64_t));
    for (int64_t i = 1; i < n; i++) { parent[i] = next_random(seed) % i; nkids[parent[i]]++; }
    Node **nodes = malloc(n * sizeof(Node *));
    for (int64_t i = 0; i < n; i++) {
        nodes[i] = malloc(sizeof(Node));
        nodes[i]->val = vals[i];
        nodes[i]->children = malloc((nkids[i] + 1) * sizeof(Node *));
        nodes[i]->nchildren = 0;
    }
    for (int64_t i = 1; i < n; i++) {
        Node *p = nodes[parent[i]];
        p->children[p->nchildren++] = nodes[i];
    }
    for (int64_t i = n - 1; i >= 1; i--) {
        int64_t j = next_random(seed) % (i + 1);
        Node *t = nodes[i]; nodes[i] = nodes[j]; nodes[j] = t;
    }
    free(vals); free(seen); free(parent); free(nkids);
    *len = n;
    return nodes;
}

int main(void) {
    int64_t seed = 1506;
    Node **trees[20];
    int64_t lens[20];
    for (int t = 0; t < 20; t++) trees[t] = random_tree(50000, &seed, &lens[t]);
    int64_t check = 0;
    for (int r = 0; r < 10; r++) {
        for (int t = 0; t < 20; t++) {
            Node **copy = malloc(lens[t] * sizeof(Node *));
            memcpy(copy, trees[t], lens[t] * sizeof(Node *));
            Node *root = find_root(copy, lens[t]);
            check = mix(check, root->val);
            free(copy);
        }
    }
    printf("200 roots over 20 trees of up to 50000 nodes: checksum %lld\n", (long long)check);
    return 0;
}
