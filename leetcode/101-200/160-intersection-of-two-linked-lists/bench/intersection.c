#include <stdio.h>
#include <stdlib.h>

static long list_length(const long *next, long head) {
    long n = 0;
    long cur = head;
    while (cur != -1) {
        n++;
        cur = next[cur];
    }
    return n;
}

static long advance(const long *next, long head, long k) {
    long cur = head;
    for (long i = 0; i < k; i++) {
        cur = next[cur];
    }
    return cur;
}

static long intersection(const long *next, long head_a, long head_b) {
    long la = list_length(next, head_a);
    long lb = list_length(next, head_b);
    long a = head_a;
    long b = head_b;
    if (la > lb) {
        a = advance(next, a, la - lb);
    } else {
        b = advance(next, b, lb - la);
    }
    while (a != -1 && b != -1) {
        if (a == b) {
            return a;
        }
        a = next[a];
        b = next[b];
    }
    return -1;
}

int main(void) {
    long n = 100003;
    long heads = n / 8;
    long passes = 280;

    long *order = malloc((size_t)n * sizeof(long));
    for (long k = 0; k < n; k++) {
        order[k] = (k * 48271) % n;
    }

    long *next = malloc((size_t)n * sizeof(long));
    for (long z = 0; z < n; z++) next[z] = -1;
    for (long j = 0; j < n - 1; j++) {
        next[order[j]] = order[j + 1];
    }

    long sink = 0;
    for (long p = 0; p < passes; p++) {
        long sa = p % heads;
        long sb = (p * 131 + 7) % heads;
        long ha = order[sa];
        long hb = order[sb];
        long idx = intersection(next, ha, hb);
        sink += idx;
    }
    printf("%ld\n", sink);
    return 0;
}
