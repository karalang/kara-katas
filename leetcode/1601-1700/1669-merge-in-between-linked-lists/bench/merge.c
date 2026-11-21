// LeetCode #1669: Merge In Between Linked Lists -- the bench's C mirror: the
// ★ arm on one list of 100000 nodes, 10000 times cut at a random place, 1
// to 8 nodes taken out and a new list of 1 to 8 put in, every cut and value
// drawn first. Every node is malloc'd on its own, and the nodes cut out are
// freed as the walk steps over them.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define START 100000
#define ROUNDS 10000

struct ListNode {
    int64_t val;
    struct ListNode *next;
};

static struct ListNode *merge_in_between(struct ListNode *list1, int64_t a, int64_t b, struct ListNode *list2) {
    struct ListNode *before = list1;
    for (int64_t i = 1; i < a; i++) before = before->next;
    struct ListNode *after = before->next;
    for (int64_t i = a; i <= b; i++) {
        struct ListNode *gone = after;
        after = after->next;
        free(gone);
    }
    struct ListNode *last = list2;
    while (last->next) last = last->next;
    before->next = list2;
    last->next = after;
    return list1;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1669;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static struct ListNode *build(const int64_t *values, int64_t n) {
    struct ListNode *head = NULL;
    for (int64_t i = n - 1; i >= 0; i--) {
        struct ListNode *node = malloc(sizeof *node);
        node->val = values[i];
        node->next = head;
        head = node;
    }
    return head;
}

int main(void) {
    static int64_t values[START];
    static int64_t cut_a[ROUNDS], cut_b[ROUNDS], cut_m[ROUNDS], list2[ROUNDS][8];
    for (int64_t i = 0; i < START; i++) values[i] = wide() % 1000001;
    int64_t len = START;
    for (int r = 0; r < ROUNDS; r++) {
        int64_t m = next_random() % 8 + 1;
        int64_t a = (next_random() * 32768 + next_random()) % (len - 2) + 1;
        int64_t room = len - 1 - a < 8 ? len - 1 - a : 8;
        int64_t b = a + next_random() % room;
        for (int64_t i = 0; i < m; i++) list2[r][i] = wide() % 1000001;
        len += m - (b - a + 1);
        cut_a[r] = a;
        cut_b[r] = b;
        cut_m[r] = m;
    }
    struct ListNode *list = build(values, START);
    for (int r = 0; r < ROUNDS; r++)
        list = merge_in_between(list, cut_a[r], cut_b[r], build(list2[r], cut_m[r]));
    int64_t nodes = 0, check = 0;
    for (struct ListNode *cur = list; cur;) {
        nodes++;
        check = (check * 31 + cur->val + 1) % 1000000007;
        struct ListNode *next = cur->next;
        free(cur);
        cur = next;
    }
    printf("%d nodes, %d merges: %lld nodes, checksum %lld\n", START, ROUNDS, (long long)nodes, (long long)check);
    return 0;
}
