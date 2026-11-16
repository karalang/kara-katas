// LeetCode #1171: Remove Zero Sum Consecutive Nodes from Linked List -- the
// bench in C, the ★ arm: prefix sums in two passes, the last node of each
// running sum kept in a hash map (open addressing over a table of 2^12
// slots, cleared for each call, the sum mixed by a multiplicative hash).
// Nodes are malloc'd as the list is built and freed after it is read. The
// same 32 lists and 400 rounds.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct ListNode {
    int64_t val;
    struct ListNode *next;
} ListNode;

#define SLOTS (1 << 12)

static int64_t keys[SLOTS];
static ListNode *vals[SLOTS];
static unsigned char used[SLOTS];

static size_t slot_of(int64_t key) {
    uint64_t x = (uint64_t)key * 0x9E3779B97F4A7C15ULL;
    size_t at = (size_t)(x >> 52);
    while (used[at] && keys[at] != key) at = (at + 1) & (SLOTS - 1);
    return at;
}

static ListNode *remove_zero_sum_sublists(ListNode *head) {
    memset(used, 0, sizeof used);
    ListNode dummy = {0, head};
    int64_t sum = 0;
    for (ListNode *cur = &dummy; cur; cur = cur->next) {
        sum += cur->val;
        size_t at = slot_of(sum);
        used[at] = 1;
        keys[at] = sum;
        vals[at] = cur;
    }
    sum = 0;
    for (ListNode *cur = &dummy; cur; cur = cur->next) {
        sum += cur->val;
        cur->next = vals[slot_of(sum)]->next;
    }
    return dummy.next;
}

static int64_t seed = 1171;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t random_value(int kind) {
    switch (kind) {
    case 0: return next_random() % 5 - 2;
    case 1: return next_random() % 11 - 5;
    case 2: return next_random() % 101 - 50;
    default: {
        int64_t size = 1 + next_random() % 3;
        return next_random() % 2 == 0 ? size : -size;
    }
    }
}

static int64_t lists[32][1000];

int main(void) {
    int rounds = 400;
    for (int l = 0; l < 32; l++)
        for (int i = 0; i < 1000; i++) lists[l][i] = random_value(l % 4);
    int64_t kept = 0, check = 0;
    // Every node of the list, kept or cut, is freed after the answer is read.
    static ListNode *all[1000];
    for (int r = 0; r < rounds; r++) {
        for (int l = 0; l < 32; l++) {
            int64_t i = next_random() % 1000;
            lists[l][i] = random_value(l % 4);
            ListNode *head = NULL;
            for (int k = 999; k >= 0; k--) {
                ListNode *n = malloc(sizeof *n);
                n->val = lists[l][k];
                n->next = head;
                head = n;
                all[k] = n;
            }
            for (ListNode *cur = remove_zero_sum_sublists(head); cur; cur = cur->next) {
                kept += 1;
                check = (check * 131 + cur->val + 1001) % 1000000007;
            }
            for (int k = 0; k < 1000; k++) free(all[k]);
        }
    }
    printf("%d rounds over 32 lists of 1000 values: %lld kept, checksum %lld\n", rounds,
           (long long)kept, (long long)check);
    return 0;
}
