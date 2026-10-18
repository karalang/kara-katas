// LeetCode #731: My Calendar II -- every booking checked in turn.
// Benchmark mirror of the Kara star arm: keep the accepted bookings and
// the stretches two of them cover, and refuse a booking that meets one
// of those stretches.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t start, end;
} Booking;

typedef struct {
    Booking *items;
    int64_t len, cap;
} List;

typedef struct {
    List booked, doubled;
} MyCalendarTwo;

static void push(List *l, int64_t start, int64_t end) {
    if (l->len == l->cap) {
        l->cap = l->cap ? l->cap * 2 : 4;
        l->items = realloc(l->items, l->cap * sizeof(Booking));
    }
    l->items[l->len++] = (Booking){start, end};
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int book(MyCalendarTwo *cal, int64_t start, int64_t end) {
    for (int64_t i = 0; i < cal->doubled.len; i++)
        if (start < cal->doubled.items[i].end && cal->doubled.items[i].start < end) return 0;
    for (int64_t i = 0; i < cal->booked.len; i++) {
        Booking b = cal->booked.items[i];
        if (start < b.end && b.start < end)
            push(&cal->doubled, start > b.start ? start : b.start, end < b.end ? end : b.end);
    }
    push(&cal->booked, start, end);
    return 1;
}

int main(void) {
    int64_t seed = 731;
    static Booking lists[20][1000];
    for (int d = 0; d < 20; d++)
        for (int i = 0; i < 1000; i++) {
            int64_t s = (next_random(&seed) * 32768 + next_random(&seed)) % 996999000;
            int64_t len = 1 + (next_random(&seed) * 32768 + next_random(&seed)) % 3000000;
            lists[d][i] = (Booking){s, s + len};
        }
    int64_t accepted = 0;
    for (int64_t round = 0; round < 80; round++)
        for (int d = 0; d < 20; d++) {
            MyCalendarTwo cal = {{NULL, 0, 0}, {NULL, 0, 0}};
            for (int i = 0; i < 1000; i++)
                accepted += book(&cal, lists[d][i].start + round, lists[d][i].end + round);
            free(cal.booked.items);
            free(cal.doubled.items);
        }
    printf("80 rounds of 20 lists of 1000 bookings: %lld accepted\n", (long long)accepted);
    return 0;
}
