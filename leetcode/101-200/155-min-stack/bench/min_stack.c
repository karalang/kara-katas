#include <stdio.h>
#include <stdlib.h>

// Kāra's min-stack modeled with two growable long arrays (value stack + parallel
// running-minimum stack), matching the .kara struct + free-function shape.
typedef struct {
    long *data;
    long *mins;
    long len;
    long cap;
} MinStack;

static void ms_reserve(MinStack *st) {
    if (st->len == st->cap) {
        st->cap = st->cap ? st->cap * 2 : 1024;
        st->data = realloc(st->data, st->cap * sizeof(long));
        st->mins = realloc(st->mins, st->cap * sizeof(long));
    }
}

static void ms_push(MinStack *st, long x) {
    ms_reserve(st);
    st->data[st->len] = x;
    if (st->len == 0 || x <= st->mins[st->len - 1]) st->mins[st->len] = x;
    else st->mins[st->len] = st->mins[st->len - 1];
    st->len++;
}

static void ms_pop(MinStack *st) {
    st->len--;
}

static long ms_top(const MinStack *st) {
    return st->data[st->len - 1];
}

static long ms_get_min(const MinStack *st) {
    return st->mins[st->len - 1];
}

int main(void) {
    long ops = 90000000L;
    long cap = 100000;

    MinStack st = {NULL, NULL, 0, 0};
    long state = 12345;
    long sz = 0;
    long sink = 0;

    for (long i = 0; i < ops; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long op = (state / 1024) % 4;
        if (sz == 0) {
            state = (state * 1103515245L + 12345L) & 2147483647L;
            long val = state % 2000000 - 1000000;
            ms_push(&st, val);
            sz++;
        } else if (sz >= cap) {
            ms_pop(&st);
            sz--;
        } else if (op == 0) {
            state = (state * 1103515245L + 12345L) & 2147483647L;
            long val = state % 2000000 - 1000000;
            ms_push(&st, val);
            sz++;
        } else if (op == 1) {
            ms_pop(&st);
            sz--;
        } else if (op == 2) {
            sink += ms_get_min(&st);
        } else {
            sink += ms_top(&st);
        }
    }
    printf("%ld\n", sink);
    free(st.data);
    free(st.mins);
    return 0;
}
