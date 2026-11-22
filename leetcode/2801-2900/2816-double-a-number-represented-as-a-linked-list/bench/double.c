// LeetCode #2816: Double a Number Represented as a Linked List -- the
// bench in C: the ★ arm over 200 numbers of 10^4 digits, all drawn first,
// then each built as a list and doubled 20 times, the list read back
// after each and freed node by node.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 200
#define N 10000

typedef struct ListNode {
    int64_t val;
    struct ListNode *next;
} ListNode;

static int64_t seed = 2816;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static ListNode *node_of(int64_t val, ListNode *next) {
    ListNode *node = malloc(sizeof *node);
    node->val = val;
    node->next = next;
    return node;
}

static ListNode *double_it(ListNode *head) {
    if (head == NULL) return NULL;
    if (head->val > 4) head = node_of(0, head);
    for (ListNode *node = head; node != NULL; node = node->next) {
        node->val = node->val * 2 % 10;
        if (node->next != NULL && node->next->val > 4) node->val += 1;
    }
    return head;
}

static ListNode *build(const int64_t *values, int n) {
    ListNode *head = NULL;
    for (int i = n - 1; i >= 0; i--) head = node_of(values[i], head);
    return head;
}

static int64_t numbers[COUNT][N];

int main(void) {
    int rounds = 20;
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < N; i++) numbers[c][i] = next_random() % 10;
        if (numbers[c][0] == 0) numbers[c][0] = next_random() % 9 + 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++)
        for (int c = 0; c < COUNT; c++) {
            ListNode *node = double_it(build(numbers[c], N));
            int64_t h = r;
            while (node != NULL) {
                total += node->val;
                h = (h * 131 + node->val) % 1000000007;
                ListNode *next = node->next;
                free(node);
                node = next;
            }
            check = (check * 31 + h) % 1000000007;
        }
    printf("%d numbers of %d digits, %d rounds: digits sum to %lld, checksum %lld\n", COUNT, N, rounds, (long long)total, (long long)check);
    return 0;
}
