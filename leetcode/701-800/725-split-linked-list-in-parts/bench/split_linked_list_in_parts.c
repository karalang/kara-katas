// LeetCode #725: Split Linked List in Parts -- count, then cut in place.
// Benchmark mirror of the Kara star arm: count the nodes, then walk the
// list once, taking each part's head, stepping to its last node and
// cutting the link after it. Nodes are plain malloc'd structs where the
// Kara program's are reference-counted.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int64_t val;
    struct Node *next;
} Node;

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static void split_list_to_parts(Node *head, int64_t k, Node **parts) {
    int64_t n = 0;
    for (Node *cur = head; cur; cur = cur->next) n++;
    int64_t size = n / k, extra = n % k;
    Node *cur = head;
    for (int64_t i = 0; i < k; i++) {
        parts[i] = cur;
        int64_t len = i < extra ? size + 1 : size;
        if (len > 0 && cur) {
            Node *tail = cur;
            for (int64_t s = 0; s < len - 1; s++)
                if (tail->next) tail = tail->next;
            cur = tail->next;
            tail->next = NULL;
        }
    }
}

// Put the parts back together, starting from part `from` and going round.
static Node *rejoin(Node **parts, int64_t k, int64_t from) {
    Node *head = NULL;
    for (int64_t i = k; i > 0;) {
        i--;
        Node *first = parts[(from + i) % k];
        if (first) {
            Node *tail = first;
            while (tail->next) tail = tail->next;
            tail->next = head;
            head = first;
        }
    }
    return head;
}

int main(void) {
    int64_t seed = 725;
    Node *lists[20];
    for (int d = 0; d < 20; d++) {
        Node *head = NULL;
        for (int j = 0; j < 1000; j++) {
            Node *node = malloc(sizeof(Node));
            node->val = next_random(&seed) % 1000;
            node->next = head;
            head = node;
        }
        lists[d] = head;
    }
    Node *parts[50];
    int64_t hash = 0;
    for (int64_t round = 0; round < 5000; round++)
        for (int64_t d = 0; d < 20; d++) {
            int64_t k = 1 + (round * 7 + d) % 50;
            split_list_to_parts(lists[d], k, parts);
            for (int64_t i = 0; i < k; i++) {
                int64_t v = parts[i] ? parts[i]->val + 1 : 0;
                hash = (hash * 31 + v) % 1000000007;
            }
            lists[d] = rejoin(parts, k, round % k);
        }
    printf("5000 rounds of 20 lists of 1000 numbers: hash %lld\n", (long long)hash);
    for (int d = 0; d < 20; d++)
        for (Node *cur = lists[d]; cur;) {
            Node *next = cur->next;
            free(cur);
            cur = next;
        }
    return 0;
}
