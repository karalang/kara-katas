// LeetCode #2807: Insert Greatest Common Divisors in Linked List -- the
// bench in C: the ★ arm over 200 lists of 5000 values up to 1000, all
// drawn first, then each built afresh from malloc'd nodes, answered, read
// and freed, 10 times.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define COUNT 200
#define N 5000

typedef struct ListNode {
    int64_t val;
    struct ListNode *next;
} ListNode;

static int64_t seed = 2807;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t gcd(int64_t a, int64_t b) {
    while (b != 0) {
        int64_t t = a % b;
        a = b;
        b = t;
    }
    return a;
}

static ListNode *node(int64_t val, ListNode *next) {
    ListNode *n = malloc(sizeof *n);
    n->val = val;
    n->next = next;
    return n;
}

static ListNode *insert_greatest_common_divisors(ListNode *head) {
    for (ListNode *cur = head; cur && cur->next; ) {
        ListNode *after = cur->next;
        cur->next = node(gcd(cur->val, after->val), after);
        cur = after;
    }
    return head;
}

static int64_t values[COUNT][N];

int main(void) {
    int rounds = 10;
    for (int t = 0; t < COUNT; t++) {
        int64_t step = t % 2 == 0 ? 12 : 1;
        for (int i = 0; i < N; i++) values[t][i] = (next_random() % (1000 / step) + 1) * step;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int t = 0; t < COUNT; t++) {
            ListNode *head = NULL;
            for (int i = N - 1; i >= 0; i--) head = node(values[t][i], head);
            head = insert_greatest_common_divisors(head);
            int64_t sum = 0;
            while (head) {
                ListNode *next = head->next;
                sum += head->val;
                free(head);
                head = next;
            }
            total += sum;
            check = (check * 31 + sum + r) % 1000000007;
        }
    }
    printf("%d lists of 5000, %d rounds: values sum to %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
