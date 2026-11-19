// LeetCode #2336: Smallest Number in Infinite Set -- the bench, the ★ arm
// in C: every number from `next` on still in the set, and the numbers
// below it that were added back kept, as C has no ordered set, in a
// binary min-heap with a flag per number for membership.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CALLS 200000

typedef struct {
    int64_t next;
    int64_t *heap;
    int64_t size;
    unsigned char *member;
} Set;

static int64_t pop_smallest(Set *s) {
    if (s->size > 0) {
        int64_t least = s->heap[0];
        int64_t last = s->heap[--s->size];
        int64_t i = 0;
        for (;;) {
            int64_t c = 2 * i + 1;
            if (c >= s->size) break;
            if (c + 1 < s->size && s->heap[c + 1] < s->heap[c]) c++;
            if (s->heap[c] >= last) break;
            s->heap[i] = s->heap[c];
            i = c;
        }
        if (s->size > 0) s->heap[i] = last;
        s->member[least] = 0;
        return least;
    }
    s->next += 1;
    return s->next - 1;
}

static void add_back(Set *s, int64_t num) {
    if (num < s->next && !s->member[num]) {
        s->member[num] = 1;
        int64_t i = s->size++;
        while (i > 0 && s->heap[(i - 1) / 2] > num) {
            s->heap[i] = s->heap[(i - 1) / 2];
            i = (i - 1) / 2;
        }
        s->heap[i] = num;
    }
}

static int64_t scrambled(int64_t index) { return index * 2654435761LL % 2147483647LL; }

int main(void) {
    static int64_t ops[CALLS];
    for (int64_t i = 0; i < CALLS; i++) {
        int64_t r = scrambled(i);
        ops[i] = r % 3 == 0 ? r / 3 % 5000 + 1 : 0;
    }
    int64_t check = 0;
    for (int pass = 0; pass < 50; pass++) {
        Set s = {1, malloc(CALLS * sizeof(int64_t)), 0, calloc(CALLS + 2, 1)};
        for (int64_t i = 0; i < CALLS; i++) {
            if (ops[i] == 0) check = (check * 31 + pop_smallest(&s)) % 1000000007;
            else add_back(&s, ops[i]);
        }
        free(s.heap);
        free(s.member);
    }
    printf("50 passes over 2*10^5 calls: checksum %lld\n", (long long)check);
    return 0;
}
