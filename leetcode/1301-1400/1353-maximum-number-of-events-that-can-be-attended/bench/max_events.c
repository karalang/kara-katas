// LeetCode #1353 bench -- C: a sweep over the days with a binary min-heap
// of the open events' last days.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int start, end;
} Event;

static Event sets[20][10000];
static Event by_start[10000];
static int heap[10000];
static int heap_len;

static int by_start_cmp(const void *a, const void *b) {
    return ((const Event *)a)->start - ((const Event *)b)->start;
}

static void push(int v) {
    int i = heap_len++;
    heap[i] = v;
    while (i > 0 && heap[(i - 1) / 2] > heap[i]) {
        int p = (i - 1) / 2, t = heap[p];
        heap[p] = heap[i];
        heap[i] = t;
        i = p;
    }
}

static void pop(void) {
    heap[0] = heap[--heap_len];
    int i = 0;
    for (;;) {
        int l = 2 * i + 1, r = l + 1, m = i;
        if (l < heap_len && heap[l] < heap[m]) m = l;
        if (r < heap_len && heap[r] < heap[m]) m = r;
        if (m == i) break;
        int t = heap[m];
        heap[m] = heap[i];
        heap[i] = t;
        i = m;
    }
}

static int max_events(Event *events, int n) {
    memcpy(by_start, events, n * sizeof(Event));
    qsort(by_start, n, sizeof(Event), by_start_cmp);
    heap_len = 0;
    int next = 0, attended = 0, day = 1;
    while (next < n || heap_len > 0) {
        if (heap_len == 0 && by_start[next].start > day) day = by_start[next].start;
        while (next < n && by_start[next].start == day) push(by_start[next++].end);
        while (heap_len > 0 && heap[0] < day) pop();
        if (heap_len > 0) {
            pop();
            attended++;
        }
        day++;
    }
    return attended;
}

int main(void) {
    long long seed = 1353;
    for (int k = 0; k < 20; k++)
        for (int i = 0; i < 10000; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            int start = 1 + (seed / 65536) % 10000;
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            sets[k][i].start = start;
            sets[k][i].end = start + (int)((seed / 65536) % 30);
        }
    long long check = 0;
    for (long long r = 0; r < 600; r++) {
        int k = check % 20, at = (check / 20) % 10000;
        int start = 1 + (check / 7) % 10000;
        sets[k][at].start = start;
        sets[k][at].end = start + (int)((check / 11) % 30);
        check = (check * 31 + max_events(sets[k], 10000) + r) % 1000000007;
    }
    printf("600 rounds over 20 sets of 10^4 events: checksum %lld\n", check);
    return 0;
}
