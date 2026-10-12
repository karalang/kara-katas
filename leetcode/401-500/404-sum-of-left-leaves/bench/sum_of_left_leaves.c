// Benchmark for #404: mirror of sum_of_left_leaves.kara (recursion that
// knows which side it came from), over the same index pool.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t val, left, right;
} Node;

static int64_t visit(const Node *nodes, int64_t node, int is_left) {
    if (node == -1) {
        return 0;
    }
    if (nodes[node].left == -1 && nodes[node].right == -1) {
        return is_left ? nodes[node].val : 0;
    }
    return visit(nodes, nodes[node].left, 1) + visit(nodes, nodes[node].right, 0);
}

static int64_t sum_of_left_leaves(const Node *nodes, int64_t n) {
    if (n == 0) {
        return 0;
    }
    return visit(nodes, 0, 0);
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(int argc, char **argv) {
    int64_t trees = argc > 1 ? atoll(argv[1]) : 50;
    int64_t n = 30000, rounds = 50;
    int64_t seed = 404, total = 0, checksum = 0;
    Node *nodes = malloc(n * sizeof(Node));
    for (int64_t t = 0; t < trees; t++) {
        nodes[0] = (Node){step(&seed) % 201 - 100, -1, -1};
        for (int64_t i = 1; i < n; i++) {
            int64_t p = step(&seed) % i;
            int64_t side = 1 + step(&seed) % 2;
            while ((side == 1 && nodes[p].left != -1) || (side == 2 && nodes[p].right != -1)) {
                p = step(&seed) % i;
                side = 1 + step(&seed) % 2;
            }
            nodes[i] = (Node){step(&seed) % 201 - 100, -1, -1};
            if (side == 1) {
                nodes[p].left = i;
            } else {
                nodes[p].right = i;
            }
        }
        for (int64_t r = 0; r < rounds; r++) {
            nodes[r].val += 1;
            int64_t s = sum_of_left_leaves(nodes, n);
            total += s;
            checksum = (checksum * 31 + s + 10000000 + r) % 1000000007;
        }
    }
    free(nodes);
    printf("%lld trees of %lld nodes, %lld rounds: total %lld, checksum %lld\n", (long long)trees, (long long)n, (long long)rounds, (long long)total, (long long)checksum);
    return 0;
}
