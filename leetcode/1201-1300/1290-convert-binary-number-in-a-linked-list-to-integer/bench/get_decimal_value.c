// LeetCode #1290 bench: the ★ arm over 10^4 lists of 30 nodes built once,
// then 500 passes, each setting one bit of every list and reading it back.
// Each node is its own allocation, as in the other languages.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

struct ListNode {
    int64_t val;
    struct ListNode *next;
};

static int64_t get_decimal_value(const struct ListNode *head) {
    int64_t value = 0;
    for (const struct ListNode *cur = head; cur != NULL; cur = cur->next) {
        value = value * 2 + cur->val;
    }
    return value;
}

static void set_bit(struct ListNode *head, int64_t k, int64_t bit) {
    int64_t i = 0;
    for (struct ListNode *cur = head; cur != NULL; cur = cur->next) {
        if (i == k) {
            cur->val = bit;
            return;
        }
        i++;
    }
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1290;
    enum { LISTS = 10000, NODES = 30 };
    struct ListNode **heads = malloc(sizeof(struct ListNode *) * LISTS);
    for (int a = 0; a < LISTS; a++) {
        struct ListNode *head = NULL;
        for (int j = 0; j < NODES; j++) {
            struct ListNode *node = malloc(sizeof(struct ListNode));
            node->val = next_random(&seed) % 2;
            node->next = head;
            head = node;
        }
        heads[a] = head;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 500; p++) {
        for (int64_t a = 0; a < LISTS; a++) {
            set_bit(heads[a], (check + a) % 30, check / 16 % 2);
            check = (check * 31 + get_decimal_value(heads[a]) + p) % 1000000007;
        }
    }
    printf("500 passes over 10^4 lists of 30 bits: checksum %lld\n", (long long)check);
    return 0;
}
