// LeetCode #1361 bench -- C: every node's parents counted, one root and
// no node with two, then a search from the root that must reach all n.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 5000
#define SETS 20

static bool validate_binary_tree_nodes(int32_t n, const int32_t *left_child, const int32_t *right_child) {
    int64_t *parents = calloc(n, sizeof *parents);
    bool *seen = calloc(n, sizeof *seen);
    int64_t *queue = malloc(sizeof *queue * (2 * (size_t)n + 1));
    bool ok = true;
    int64_t root = -1;
    for (int64_t i = 0; i < n; i++) {
        int32_t kids[2] = {left_child[i], right_child[i]};
        for (int k = 0; k < 2; k++)
            if (kids[k] != -1) parents[kids[k]] += 1;
    }
    for (int64_t i = 0; i < n && ok; i++) {
        if (parents[i] > 1) ok = false;
        else if (parents[i] == 0) {
            if (root != -1) ok = false;
            else root = i;
        }
    }
    if (ok && root == -1) ok = false;
    int64_t head = 0, tail = 0;
    if (ok) {
        queue[tail++] = root;
        while (head < tail) {
            int64_t node = queue[head++];
            if (seen[node]) {
                ok = false;
                break;
            }
            seen[node] = true;
            int32_t kids[2] = {left_child[node], right_child[node]};
            for (int k = 0; k < 2; k++)
                if (kids[k] != -1) queue[tail++] = kids[k];
        }
        if (ok) ok = head == n;
    }
    free(parents);
    free(seen);
    free(queue);
    return ok;
}

static int64_t seed = 1361;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

// n nodes made into one binary tree, each node after the first hung on a
// free side of a node already placed; then, one time in two, broken or not
static void random_case(int64_t n, int32_t *left, int32_t *right) {
    int64_t *order = malloc(sizeof *order * n);
    for (int64_t i = 0; i < n; i++) {
        left[i] = -1;
        right[i] = -1;
        order[i] = i;
    }
    for (int64_t i = 1; i < n; i++) {
        int64_t j = next_random() % (i + 1);
        int64_t held = order[i];
        order[i] = order[j];
        order[j] = held;
    }
    for (int64_t i = 1; i < n; i++) {
        for (;;) {
            int64_t parent = order[next_random() % i];
            if (next_random() % 2 == 0) {
                if (left[parent] == -1) {
                    left[parent] = (int32_t)order[i];
                    break;
                }
            } else if (right[parent] == -1) {
                right[parent] = (int32_t)order[i];
                break;
            }
        }
    }
    int64_t node = next_random() % n;
    int32_t other = (int32_t)(next_random() % n);
    switch (next_random() % 6) {
    case 0:
        if (left[node] == -1) left[node] = other;
        else if (right[node] == -1) right[node] = other;
        break;
    case 1:
        left[node] = -1;
        break;
    case 2:
        if (right[node] != -1) right[node] = other;
        break;
    default:
        break;
    }
    free(order);
}

int main(void) {
    // 20 sets of 5000 nodes made once; then 5000 questions, each set drawn
    // from the checksum so far, every answer folded into it
    static int32_t left[SETS][N], right[SETS][N];
    for (int s = 0; s < SETS; s++) random_case(N, left[s], right[s]);
    int64_t check = 0;
    for (int64_t r = 0; r < 5000; r++) {
        int64_t s = check % SETS;
        bool got = validate_binary_tree_nodes(N, left[s], right[s]);
        check = (check * 31 + (got ? 1 : 0) + r) % 1000000007;
    }
    printf("5000 questions: checksum %lld\n", (long long)check);
    return 0;
}
