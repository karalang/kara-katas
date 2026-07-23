#include <stdio.h>
#include <stdlib.h>

static long split_mid(long *nxt, long head) {
    long slow = head;
    long fast = nxt[head];
    while (fast != -1) {
        fast = nxt[fast];
        if (fast != -1) {
            slow = nxt[slow];
            fast = nxt[fast];
        }
    }
    long mid = nxt[slow];
    nxt[slow] = -1;
    return mid;
}

static long merge(const long *val, long *nxt, long a, long b) {
    long ai = a, bi = b, head = -1, tail = -1;
    while (ai != -1 && bi != -1) {
        if (val[ai] <= val[bi]) {
            if (head == -1) head = ai; else nxt[tail] = ai;
            tail = ai;
            ai = nxt[ai];
        } else {
            if (head == -1) head = bi; else nxt[tail] = bi;
            tail = bi;
            bi = nxt[bi];
        }
    }
    long rest = (ai != -1) ? ai : bi;
    if (tail != -1) {
        if (rest == -1) nxt[tail] = -1; else nxt[tail] = rest;
    }
    return head;
}

static long sort_chain(const long *val, long *nxt, long head) {
    if (head == -1) return -1;
    if (nxt[head] == -1) return head;
    long mid = split_mid(nxt, head);
    long left = sort_chain(val, nxt, head);
    long right = sort_chain(val, nxt, mid);
    return merge(val, nxt, left, right);
}

int main(void) {
    long n = 20000, passes = 180, vr = 100000;
    long *val = malloc(n * sizeof(long));
    long *nxt = malloc(n * sizeof(long));
    long state = 12345;
    for (long i = 0; i < n; i++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        val[i] = state % vr;
        nxt[i] = -1;
    }

    long sink = 0;
    for (long p = 0; p < passes; p++) {
        state = (state * 1103515245L + 12345L) & 2147483647L;
        long idx = state % n;
        state = (state * 1103515245L + 12345L) & 2147483647L;
        val[idx] = state % vr;

        for (long i = 0; i < n - 1; i++) nxt[i] = i + 1;
        nxt[n - 1] = -1;

        long head = sort_chain(val, nxt, 0);

        long cur = head;
        long pos = 1;
        while (cur != -1) {
            sink += pos * val[cur];
            pos++;
            cur = nxt[cur];
        }
    }
    printf("%ld\n", sink);
    free(val);
    free(nxt);
    return 0;
}
