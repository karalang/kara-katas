// LeetCode #1019: Next Greater Node In Linked List -- bench
// Mirrors next_greater.kara; see ../README.md § Benchmarks.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

struct ListNode {
    int64_t val;
    struct ListNode *next;
};

// the answers for the list at `head`, in a fresh array the caller frees;
// its length goes to *len
static int64_t *next_larger_nodes(const struct ListNode *head, int64_t *len) {
    int64_t cap = 16, n = 0, top = 0;
    int64_t *values = malloc((size_t)cap * sizeof(int64_t));
    int64_t *answer = malloc((size_t)cap * sizeof(int64_t));
    int64_t *waiting = malloc((size_t)cap * sizeof(int64_t));
    for (const struct ListNode *cur = head; cur != NULL; cur = cur->next) {
        int64_t v = cur->val;
        while (top > 0 && values[waiting[top - 1]] < v) {
            answer[waiting[--top]] = v;
        }
        if (n == cap) {
            cap *= 2;
            values = realloc(values, (size_t)cap * sizeof(int64_t));
            answer = realloc(answer, (size_t)cap * sizeof(int64_t));
            waiting = realloc(waiting, (size_t)cap * sizeof(int64_t));
        }
        waiting[top++] = n;
        values[n] = v;
        answer[n] = 0;
        n++;
    }
    free(values);
    free(waiting);
    *len = n;
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    int64_t count = 500;
    int64_t rounds = 10;
    int64_t seed = 1019;
    struct ListNode **lists = malloc((size_t)count * sizeof(struct ListNode *));
    int64_t nodes = 0;
    for (int64_t t = 0; t < count; t++) {
        int64_t len = next_random(&seed) % 10000 + 1;
        int64_t *values = malloc((size_t)len * sizeof(int64_t));
        for (int64_t i = 0; i < len; i++) {
            int64_t hi = next_random(&seed);
            values[i] = (hi * 32768 + next_random(&seed)) % 1000000000 + 1;
        }
        nodes += len;
        struct ListNode *head = NULL;
        for (int64_t k = len - 1; k >= 0; k--) {
            struct ListNode *node = malloc(sizeof(struct ListNode));
            node->val = values[k];
            node->next = head;
            head = node;
        }
        lists[t] = head;
        free(values);
    }
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t t = 0; t < count; t++) {
            int64_t len;
            int64_t *answer = next_larger_nodes(lists[t], &len);
            for (int64_t i = 0; i < len; i++) {
                total = (total + answer[i]) % 1000000007;
                check = (check * 31 + answer[i]) % 1000000007;
            }
            free(answer);
        }
    }
    printf("%lld lists, %lld nodes, %lld rounds: answer sum %lld, checksum %lld\n",
           (long long)count, (long long)nodes, (long long)rounds, (long long)total,
           (long long)check);
    return 0;
}
