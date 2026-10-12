// Benchmark for #430: mirror of flatten.kara (recursion). Nodes are
// malloc'd; the walk frees each node as it passes, where the Kāra
// program breaks its links and the count drops to zero.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int64_t val;
    struct Node *prev, *next, *child;
} Node;

static Node *flatten_level(Node *head) {
    Node *cur = head;
    for (;;) {
        Node *after = cur->next;
        if (cur->child) {
            Node *c = cur->child;
            Node *child_tail = flatten_level(c);
            cur->next = c;
            c->prev = cur;
            cur->child = NULL;
            if (after) {
                child_tail->next = after;
                after->prev = child_tail;
            } else {
                return child_tail;
            }
        }
        if (after) cur = after;
        else return cur;
    }
}

static Node *flatten(Node *head) {
    if (head) flatten_level(head);
    return head;
}

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static Node *make_level(int64_t length, int64_t *budget, int64_t depth, int64_t *next_val, int64_t *seed) {
    Node *head = NULL, *last = NULL;
    for (int64_t i = 0; i < length; i++) {
        if (*budget == 0) break;
        *budget -= 1;
        Node *node = calloc(1, sizeof *node);
        node->val = (*next_val)++;
        if (depth < 6 && *budget > 0 && step(seed) % 4 == 0) {
            int64_t child_length = 1 + step(seed) % 8;
            node->child = make_level(child_length, budget, depth + 1, next_val, seed);
        }
        if (last) {
            last->next = node;
            node->prev = last;
        } else {
            head = node;
        }
        last = node;
    }
    return head;
}

int main(int argc, char **argv) {
    int64_t n = 1000;
    int64_t rounds = argc > 1 ? atoll(argv[1]) : 2000;
    int64_t seed = 430;
    int64_t misplaced = 0, checksum = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t budget = n, next_val = 1;
        Node *cur = flatten(make_level(n, &budget, 0, &next_val, &seed));
        int64_t expect = 1;
        while (cur) {
            if (cur->val != expect) misplaced++;
            expect++;
            checksum = (checksum * 31 + cur->val) % 1000000007;
            Node *next = cur->next;
            free(cur);
            cur = next;
        }
    }
    printf("%lld rounds of %lld nodes: %lld misplaced, checksum %lld\n", (long long)rounds, (long long)n, (long long)misplaced, (long long)checksum);
    return 0;
}
