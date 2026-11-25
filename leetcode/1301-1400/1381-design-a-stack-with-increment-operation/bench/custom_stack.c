// LeetCode #1381 bench -- C: the ★ arm: an increment is owed to the
// element k places up; a pop pays the top element what it is owed and
// hands the debt down to the one below. Fixed arrays of the stack's size.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int max_size, top;
    int *stack, *owed;
} CustomStack;

static void stack_init(CustomStack *s, int max_size) {
    s->max_size = max_size;
    s->top = 0;
    s->stack = malloc(sizeof(int) * max_size);
    s->owed = malloc(sizeof(int) * max_size);
}

static void stack_free(CustomStack *s) {
    free(s->stack);
    free(s->owed);
}

static void stack_push(CustomStack *s, int x) {
    if (s->top < s->max_size) {
        s->stack[s->top] = x;
        s->owed[s->top] = 0;
        s->top++;
    }
}

static int stack_pop(CustomStack *s) {
    if (s->top == 0) return -1;
    s->top--;
    int debt = s->owed[s->top];
    if (s->top > 0) s->owed[s->top - 1] += debt;
    return s->stack[s->top] + debt;
}

static void stack_increment(CustomStack *s, int k, int val) {
    int reach = s->top < k ? s->top : k;
    if (reach > 0) s->owed[reach - 1] += val;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1381, check = 0;
    for (int round = 0; round < 2000; round++) {
        seed = (seed + check) % 2147483648LL;
        CustomStack s;
        stack_init(&s, 1000);
        for (int c = 0; c < 3000; c++) {
            int64_t r = next_random(&seed) % 10;
            if (r < 4) {
                stack_push(&s, (int)(1 + next_random(&seed) % 1000));
            } else if (r < 7) {
                int64_t k = 1 + next_random(&seed) % 1000;
                int64_t val = next_random(&seed) % 101;
                stack_increment(&s, (int)k, (int)val);
            } else {
                check = (check * 131 + stack_pop(&s) + 1) % 1000000007;
            }
        }
        stack_free(&s);
    }
    printf("2000 rounds of 3000 calls on a stack of 1000: checksum %lld\n", (long long)check);
    return 0;
}
