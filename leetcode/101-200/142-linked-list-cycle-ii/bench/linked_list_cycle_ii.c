#include <stdio.h>
#include <stdlib.h>

// Build-once + punch Floyd two-phase cycle-entry detection over an index-pool of
// K lists (see linked_list_cycle_ii.kara). nxt[i] = next global index or -1.
static long *nxt;

// Returns the local cycle-entry index (0..len-1), or -1 if acyclic. base==head.
static long detect(long head) {
    long slow = head, fast = head;
    int met = 0;
    for (;;) {
        fast = nxt[fast];
        if (fast < 0) return -1;
        fast = nxt[fast];
        if (fast < 0) return -1;
        slow = nxt[slow];
        if (slow == fast) { met = 1; break; }
    }
    if (!met) return -1;
    slow = head;
    while (slow != fast) {
        slow = nxt[slow];
        fast = nxt[fast];
    }
    return slow - head;
}

int main(void) {
    long k_lists = 1000;
    long len = 60;
    long passes = 3000;
    long cycpct = 50;
    long pool = k_lists * len;

    nxt = malloc((size_t)pool * sizeof(long));
    long *target = malloc((size_t)k_lists * sizeof(long));
    long *tail = malloc((size_t)k_lists * sizeof(long));

    long state = 12345;

    for (long k = 0; k < k_lists; k++) {
        long base = k * len;
        for (long j = 0; j < len - 1; j++) nxt[base + j] = base + j + 1;
        long t = base + len - 1;
        tail[k] = t;

        state = (state * 1103515245 + 12345) & 2147483647;
        long coin = (state >> 16) % 100;
        state = (state * 1103515245 + 12345) & 2147483647;
        long tl = (state >> 16) % len;
        target[k] = base + tl;

        if (coin < cycpct) nxt[t] = base + tl;
        else nxt[t] = -1;
    }

    long sink = 0;
    for (long pass = 0; pass < passes; pass++) {
        long idx = pass % k_lists;
        long ti = tail[idx];
        if (nxt[ti] < 0) nxt[ti] = target[idx];
        else nxt[ti] = -1;

        for (long kk = 0; kk < k_lists; kk++) {
            long e = detect(kk * len);
            sink += e + 1;
        }
    }

    printf("%ld\n", sink);
    return 0;
}
