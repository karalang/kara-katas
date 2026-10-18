// LeetCode #707: Design Linked List -- singly linked, with a sentinel.
// Benchmark mirror of the Kara star arm: walk to the node before the
// position, then link a new node in after it or link past the next.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int64_t val;
    struct Node *next;
} Node;

typedef struct {
    Node head;
    int64_t size;
} MyLinkedList;

static Node *before(MyLinkedList *list, int64_t index) {
    Node *at = &list->head;
    for (int64_t i = 0; i < index; i++) {
        at = at->next;
    }
    return at;
}

static int64_t get(MyLinkedList *list, int64_t index) {
    if (index < 0 || index >= list->size) {
        return -1;
    }
    return before(list, index)->next->val;
}

static void add_at_index(MyLinkedList *list, int64_t index, int64_t val) {
    if (index < 0 || index > list->size) {
        return;
    }
    Node *prev = before(list, index);
    Node *node = malloc(sizeof(Node));
    node->val = val;
    node->next = prev->next;
    prev->next = node;
    list->size += 1;
}

static void add_at_head(MyLinkedList *list, int64_t val) { add_at_index(list, 0, val); }

static void add_at_tail(MyLinkedList *list, int64_t val) { add_at_index(list, list->size, val); }

static void delete_at_index(MyLinkedList *list, int64_t index) {
    if (index < 0 || index >= list->size) {
        return;
    }
    Node *prev = before(list, index);
    Node *gone = prev->next;
    prev->next = gone->next;
    free(gone);
    list->size -= 1;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 707;
    int64_t values = 0;
    int64_t checksum = 0;
    for (int round = 0; round < 5; round++) {
        for (int list_no = 0; list_no < 10; list_no++) {
            MyLinkedList list = {{0, NULL}, 0};
            for (int i = 0; i < 6000; i++) {
                int64_t op = next_random(&seed) % 5;
                int64_t index = next_random(&seed) % (list.size + 3);
                int64_t val = next_random(&seed) % 1001;
                if (op == 0) {
                    checksum = (checksum * 31 + get(&list, index) + 2) % 1000000007;
                } else if (op == 1) {
                    add_at_head(&list, val);
                } else if (op == 2) {
                    add_at_tail(&list, val);
                } else if (op == 3) {
                    add_at_index(&list, index, val);
                } else {
                    delete_at_index(&list, index);
                }
            }
            values += list.size;
            Node *at = list.head.next;
            while (at != NULL) {
                Node *next = at->next;
                free(at);
                at = next;
            }
        }
    }
    printf("5 rounds of 10 lists of 6000 calls: %lld values left, checksum %lld\n",
           (long long)values, (long long)checksum);
    return 0;
}
