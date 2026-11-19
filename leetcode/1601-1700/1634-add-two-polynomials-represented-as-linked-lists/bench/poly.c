// LeetCode #1634: Add Two Polynomials Represented as Linked Lists -- the
// bench's C mirror: the ★ arm on 10 random pairs of polynomials with
// powers below 400000, all drawn first as terms; each pair is built into
// two lists of malloc'd nodes, added, and every node freed as it is read.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

enum { PAIRS = 10, POWERS = 400000 };

typedef struct PolyNode {
    int64_t coefficient, power;
    struct PolyNode *next;
} PolyNode;

static PolyNode *node_new(int64_t coefficient, int64_t power, PolyNode *next) {
    PolyNode *n = malloc(sizeof(PolyNode));
    n->coefficient = coefficient;
    n->power = power;
    n->next = next;
    return n;
}

// the sum as a new list; the inputs are freed as they are walked, as the
// other languages release theirs
static PolyNode *add_poly(PolyNode *a, PolyNode *b) {
    PolyNode head = {0, 0, NULL}, *tail = &head;
    while (a || b) {
        int64_t coefficient, power;
        PolyNode *x = NULL, *y = NULL;
        if (a && b && a->power == b->power) {
            coefficient = a->coefficient + b->coefficient, power = a->power;
            x = a, y = b, a = a->next, b = b->next;
        } else if (a && b && a->power < b->power) {
            coefficient = b->coefficient, power = b->power;
            y = b, b = b->next;
        } else if (a) {
            coefficient = a->coefficient, power = a->power;
            x = a, a = a->next;
        } else {
            coefficient = b->coefficient, power = b->power;
            y = b, b = b->next;
        }
        free(x);
        free(y);
        if (coefficient != 0) {
            tail->next = node_new(coefficient, power, NULL);
            tail = tail->next;
        }
    }
    return head.next;
}

static int64_t seed = 1634;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

typedef struct {
    int64_t (*terms)[2];
    size_t len;
} Terms;

static PolyNode *from_terms(Terms t) {
    PolyNode *head = NULL;
    for (size_t i = t.len; i-- > 0;) head = node_new(t.terms[i][0], t.terms[i][1], head);
    return head;
}

static Terms random_terms(void) {
    Terms t = {malloc(sizeof(int64_t[2]) * POWERS), 0};
    for (int64_t power = POWERS - 1; power >= 0; power--) {
        if (next_random() % 2 == 0) {
            int64_t coefficient = next_random() % 6 - 3;
            if (coefficient >= 0) coefficient++;
            t.terms[t.len][0] = coefficient;
            t.terms[t.len][1] = power;
            t.len++;
        }
    }
    return t;
}

int main(void) {
    Terms pairs[PAIRS][2];
    for (int i = 0; i < PAIRS; i++) {
        pairs[i][0] = random_terms();
        pairs[i][1] = random_terms();
    }
    int64_t check = 0, terms = 0;
    for (int i = 0; i < PAIRS; i++) {
        PolyNode *node = add_poly(from_terms(pairs[i][0]), from_terms(pairs[i][1]));
        while (node) {
            terms++;
            check = ((check * 31 + node->coefficient + 1000000) % 1000000007 * 31 + node->power) % 1000000007;
            PolyNode *next = node->next;
            free(node);
            node = next;
        }
    }
    for (int i = 0; i < PAIRS; i++) {
        free(pairs[i][0].terms);
        free(pairs[i][1].terms);
    }
    printf("10 pairs of up to 400000 terms: %lld terms, checksum %lld\n", (long long)terms, (long long)check);
    return 0;
}
