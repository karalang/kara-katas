// Benchmark for #445: mirror of add_two_numbers.kara (two stacks) on 100
// random numbers of 1,000 to 2,000 digits, built once; 60 rounds add each
// to the next. Each sum is freed after it is read, as Kāra drops it.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct ListNode {
    int64_t val;
    struct ListNode *next;
} ListNode;

static ListNode *node_new(int64_t val, ListNode *next) {
    ListNode *n = malloc(sizeof(ListNode));
    n->val = val;
    n->next = next;
    return n;
}

static void list_free(ListNode *n) {
    while (n) {
        ListNode *next = n->next;
        free(n);
        n = next;
    }
}

typedef struct {
    int64_t *data;
    int64_t len, cap;
} Stack;

static void push(Stack *s, int64_t v) {
    if (s->len == s->cap) {
        s->cap = s->cap ? s->cap * 2 : 4;
        s->data = realloc(s->data, s->cap * sizeof(int64_t));
    }
    s->data[s->len++] = v;
}

static ListNode *add_two_numbers(const ListNode *l1, const ListNode *l2) {
    Stack a = {0}, b = {0};
    for (const ListNode *n = l1; n; n = n->next) {
        push(&a, n->val);
    }
    for (const ListNode *n = l2; n; n = n->next) {
        push(&b, n->val);
    }
    ListNode *sum = NULL;
    int64_t carry = 0;
    while (a.len > 0 || b.len > 0 || carry > 0) {
        int64_t digit = carry;
        if (a.len > 0) {
            digit += a.data[--a.len];
        }
        if (b.len > 0) {
            digit += b.data[--b.len];
        }
        sum = node_new(digit % 10, sum);
        carry = digit / 10;
    }
    free(a.data);
    free(b.data);
    return sum;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 100, rounds = 60;
    int64_t seed = 445;
    ListNode **numbers = malloc(count * sizeof(ListNode *));
    for (int64_t c = 0; c < count; c++) {
        int64_t length = 1000 + next_random(&seed) % 1001;
        int64_t *digits = malloc(length * sizeof(int64_t));
        for (int64_t i = 0; i < length; i++) {
            int64_t d = next_random(&seed) % 2 == 0 ? 9 : next_random(&seed) % 10;
            if (i == 0 && d == 0) {
                d = 1;
            }
            digits[i] = d;
        }
        ListNode *head = NULL;
        for (int64_t i = length - 1; i >= 0; i--) {
            head = node_new(digits[i], head);
        }
        numbers[c] = head;
        free(digits);
    }
    int64_t total_digits = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        for (int64_t i = 0; i < count; i++) {
            ListNode *sum = add_two_numbers(numbers[i], numbers[(i + 1) % count]);
            for (ListNode *n = sum; n; n = n->next) {
                total_digits++;
                checksum = (checksum * 31 + n->val + round) % 1000000007;
            }
            list_free(sum);
        }
    }
    printf("%lld rounds on %lld numbers: %lld digits, checksum %lld\n", (long long)rounds,
           (long long)count, (long long)total_digits, (long long)checksum);
    for (int64_t c = 0; c < count; c++) {
        list_free(numbers[c]);
    }
    free(numbers);
    return 0;
}
