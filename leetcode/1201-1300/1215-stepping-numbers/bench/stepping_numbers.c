// LeetCode #1215 bench, in C: the ★ arm (a breadth-first search from the
// digits 1 to 9, each number followed by itself with one more digit,
// stopping at the first number past `high`) on 2000 random ranges inside
// 0 to 2 * 10^9, drawn once; then 20 rounds over the ranges, each
// answer's length and last number folded into a checksum.

#include <stdio.h>
#include <stdlib.h>

static long long seed = 1215;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct {
    long long *v;
    long long n, cap;
} vec_t;

static void push(vec_t *v, long long x) {
    if (v->n == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 16;
        v->v = realloc(v->v, v->cap * sizeof(long long));
    }
    v->v[v->n++] = x;
}

static vec_t count_stepping_numbers(long long low, long long high) {
    vec_t out = {0}, queue = {0};
    if (low == 0) push(&out, 0);
    for (long long d = 1; d < 10; d++) push(&queue, d);
    long long head = 0;
    while (head < queue.n) {
        long long n = queue.v[head++];
        if (n > high) break;
        if (n >= low) push(&out, n);
        long long last = n % 10;
        if (last > 0) push(&queue, n * 10 + last - 1);
        if (last < 9) push(&queue, n * 10 + last + 1);
    }
    free(queue.v);
    return out;
}

int main(void) {
    long long lows[2000], highs[2000];
    for (int i = 0; i < 2000; i++) {
        long long a = next_random();
        long long b = next_random();
        lows[i] = (a * 32768 + b) % 2000000001LL;
        long long c = next_random();
        long long d = next_random();
        highs[i] = lows[i] + (c * 32768 + d) % (2000000001LL - lows[i]);
    }
    long long check = 0;
    for (long long round = 0; round < 20; round++)
        for (int i = 0; i < 2000; i++) {
            vec_t answer = count_stepping_numbers(lows[i], highs[i]);
            long long last = answer.n > 0 ? answer.v[answer.n - 1] : -1;
            check = (check * 131 + answer.n + last % 1000003 + round) % 1000000007LL;
            free(answer.v);
        }
    printf("20 rounds over 2000 ranges: checksum %lld\n", check);
    return 0;
}
