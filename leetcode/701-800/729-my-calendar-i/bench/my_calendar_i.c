// LeetCode #729: My Calendar I -- every booking checked in turn.
// Benchmark mirror of the Kara star arm: keep the accepted bookings in
// a list and accept a new one only if it overlaps none of them.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t start, end;
} Booking;

typedef struct {
    Booking *booked;
    int64_t len, cap;
} MyCalendar;

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static int book(MyCalendar *cal, int64_t start, int64_t end) {
    for (int64_t i = 0; i < cal->len; i++)
        if (start < cal->booked[i].end && cal->booked[i].start < end) return 0;
    if (cal->len == cal->cap) {
        cal->cap = cal->cap ? cal->cap * 2 : 4;
        cal->booked = realloc(cal->booked, cal->cap * sizeof(Booking));
    }
    cal->booked[cal->len++] = (Booking){start, end};
    return 1;
}

int main(void) {
    int64_t seed = 729;
    static Booking lists[20][1000];
    for (int d = 0; d < 20; d++)
        for (int i = 0; i < 1000; i++) {
            int64_t s = (next_random(&seed) * 32768 + next_random(&seed)) % 998999000;
            int64_t len = 1 + (next_random(&seed) * 32768 + next_random(&seed)) % 1000000;
            lists[d][i] = (Booking){s, s + len};
        }
    int64_t accepted = 0;
    for (int64_t round = 0; round < 80; round++)
        for (int d = 0; d < 20; d++) {
            MyCalendar cal = {NULL, 0, 0};
            for (int i = 0; i < 1000; i++)
                accepted += book(&cal, lists[d][i].start + round, lists[d][i].end + round);
            free(cal.booked);
        }
    printf("80 rounds of 20 lists of 1000 bookings: %lld accepted\n", (long long)accepted);
    return 0;
}
