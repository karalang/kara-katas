// LeetCode #1229 bench: the ★ arm in C, over the same 50 pairs of
// schedules and 10 durations as the Kāra bench. A slot is a pair of longs;
// each solve copies and sorts both lists, as the Kāra arm does.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { long start, end; } Slot;

static int by_slot(const void *x, const void *y) {
    const Slot *a = x, *b = y;
    if (a->start != b->start) return a->start < b->start ? -1 : 1;
    if (a->end != b->end) return a->end < b->end ? -1 : 1;
    return 0;
}

// Returns the start of the earliest meeting, or -1 for none.
static long min_available_duration(const Slot *s1, long n, const Slot *s2, long m, long duration) {
    Slot *a = malloc(sizeof(Slot) * n), *b = malloc(sizeof(Slot) * m);
    memcpy(a, s1, sizeof(Slot) * n);
    memcpy(b, s2, sizeof(Slot) * m);
    qsort(a, n, sizeof(Slot), by_slot);
    qsort(b, m, sizeof(Slot), by_slot);
    long i = 0, j = 0, found = -1;
    while (i < n && j < m) {
        long start = a[i].start > b[j].start ? a[i].start : b[j].start;
        long end = a[i].end < b[j].end ? a[i].end : b[j].end;
        if (end - start >= duration) {
            found = start;
            break;
        }
        if (a[i].end < b[j].end)
            i++;
        else
            j++;
    }
    free(a);
    free(b);
    return found;
}

static long next_random(long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648L;
    return *seed / 65536;
}

static void slots(long *seed, Slot *out, long count, long width, long gap) {
    long at = next_random(seed) % (gap + 1);
    for (long k = 0; k < count; k++) {
        long end = at + next_random(seed) % width + 1;
        out[k] = (Slot){at, end};
        at = end + next_random(seed) % gap + 1;
    }
    for (long i = count - 1; i >= 1; i--) {
        long j = next_random(seed) % (i + 1);
        Slot t = out[i];
        out[i] = out[j];
        out[j] = t;
    }
}

int main(void) {
    long seed = 1229;
    Slot *all = malloc(sizeof(Slot) * 100 * 10000);
    for (int p = 0; p < 50; p++) {
        slots(&seed, all + (long)(2 * p) * 10000, 10000, 50000, 50000);
        slots(&seed, all + (long)(2 * p + 1) * 10000, 10000, 50000, 50000);
    }
    long check = 0;
    for (int p = 0; p < 50; p++)
        for (long k = 1; k <= 10; k++) {
            long start = min_available_duration(all + (long)(2 * p) * 10000, 10000, all + (long)(2 * p + 1) * 10000, 10000, k * 4000);
            long v = start < 0 ? 7 : start;
            check = (check * 131 + v) % 1000000007;
        }
    printf("50 pairs of 10^4 slots, 10 durations: checksum %ld\n", check);
    free(all);
    return 0;
}
