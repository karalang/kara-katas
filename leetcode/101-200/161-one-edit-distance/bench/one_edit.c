#include <stdio.h>
#include <stdlib.h>

static long *buf_a;
static long *buf_b;
static long *len_a;
static long *len_b;

static int tails_equal(const long *s, const long *l, long ss, long se, long ls, long le) {
    long a = ss, b = ls;
    while (a < se && b < le) {
        if (s[a] != l[b]) return 0;
        a++;
        b++;
    }
    return a == se && b == le;
}

static int check(const long *s, long so, long m, const long *l, long lo, long n) {
    if (n - m > 1) return 0;
    for (long i = 0; i < m; i++) {
        if (s[so + i] != l[lo + i]) {
            if (m == n) {
                return tails_equal(s, l, so + i + 1, so + m, lo + i + 1, lo + n);
            }
            return tails_equal(s, l, so + i, so + m, lo + i + 1, lo + n);
        }
    }
    return n - m == 1;
}

static int is_one_edit(const long *a, long oa, long la, const long *b, long ob, long lb) {
    if (la <= lb) return check(a, oa, la, b, ob, lb);
    return check(b, ob, lb, a, oa, la);
}

int main(void) {
    long pairs = 4000;
    long l = 48;
    long reps = 3000;
    long stride = l + 2;
    long cap = pairs * stride;

    buf_a = calloc((size_t)cap, sizeof(long));
    buf_b = calloc((size_t)cap, sizeof(long));
    len_a = calloc((size_t)pairs, sizeof(long));
    len_b = calloc((size_t)pairs, sizeof(long));

    long state = 12345;
    for (long pi = 0; pi < pairs; pi++) {
        long oa = pi * stride;
        long ob = pi * stride;
        for (long k = 0; k < l; k++) {
            state = (state * 1103515245 + 12345) & 2147483647;
            buf_a[oa + k] = state % 26;
        }
        len_a[pi] = l;
        state = (state * 1103515245 + 12345) & 2147483647;
        long kind = state % 4;
        if (kind == 0) {
            for (long j = 0; j < l; j++) buf_b[ob + j] = buf_a[oa + j];
            state = (state * 1103515245 + 12345) & 2147483647;
            long pos = state % l;
            buf_b[ob + pos] = (buf_a[oa + pos] + 1) % 26;
            len_b[pi] = l;
        } else if (kind == 1) {
            state = (state * 1103515245 + 12345) & 2147483647;
            long pos = state % (l + 1);
            for (long j = 0; j < pos; j++) buf_b[ob + j] = buf_a[oa + j];
            state = (state * 1103515245 + 12345) & 2147483647;
            buf_b[ob + pos] = state % 26;
            for (long t = pos; t < l; t++) buf_b[ob + t + 1] = buf_a[oa + t];
            len_b[pi] = l + 1;
        } else if (kind == 2) {
            state = (state * 1103515245 + 12345) & 2147483647;
            long pos = state % l;
            long w = 0;
            for (long j = 0; j < l; j++) {
                if (j != pos) {
                    buf_b[ob + w] = buf_a[oa + j];
                    w++;
                }
            }
            len_b[pi] = l - 1;
        } else {
            for (long j = 0; j < l; j++) buf_b[ob + j] = buf_a[oa + j];
            state = (state * 1103515245 + 12345) & 2147483647;
            long p1 = state % l;
            state = (state * 1103515245 + 12345) & 2147483647;
            long p2 = (p1 + 1 + state % (l - 1)) % l;
            buf_b[ob + p1] = (buf_a[oa + p1] + 1) % 26;
            buf_b[ob + p2] = (buf_a[oa + p2] + 1) % 26;
            len_b[pi] = l;
        }
    }

    long sink = 0;
    for (long rep = 0; rep < reps; rep++) {
        long idx = rep % pairs;
        long col = (rep * 7 + 3) % l;
        long oa = idx * stride;
        buf_a[oa + col] = (buf_a[oa + col] + 1) % 26;
        for (long i = 0; i < pairs; i++) {
            long o = i * stride;
            if (is_one_edit(buf_a, o, len_a[i], buf_b, o, len_b[i])) {
                sink++;
            }
        }
    }
    printf("%ld\n", sink);
    return 0;
}
