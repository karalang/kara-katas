// LeetCode #732: My Calendar III -- starts and ends, merged.
// Benchmark mirror of the Kara star arm: keep the starts and the ends
// in two sorted arrays, each put in its place by binary search, and
// sweep both together for the most bookings at once.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int64_t *items;
    int64_t len, cap;
} List;

typedef struct {
    List starts, ends;
} MyCalendarThree;

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static void place(List *v, int64_t x) {
    int64_t lo = 0, hi = v->len;
    while (lo < hi) {
        int64_t mid = (lo + hi) / 2;
        if (v->items[mid] <= x) lo = mid + 1;
        else hi = mid;
    }
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->items = realloc(v->items, v->cap * sizeof(int64_t));
    }
    memmove(v->items + lo + 1, v->items + lo, (v->len - lo) * sizeof(int64_t));
    v->items[lo] = x;
    v->len++;
}

static int64_t book(MyCalendarThree *cal, int64_t start, int64_t end) {
    place(&cal->starts, start);
    place(&cal->ends, end);
    int64_t n = cal->starts.len, i = 0, j = 0, now = 0, most = 0;
    while (i < n) {
        if (cal->ends.items[j] <= cal->starts.items[i]) {
            now--;
            j++;
        } else {
            now++;
            i++;
            if (now > most) most = now;
        }
    }
    return most;
}

int main(void) {
    int64_t seed = 732;
    static int64_t ls[20][1000], le[20][1000];
    for (int d = 0; d < 20; d++)
        for (int i = 0; i < 1000; i++) {
            int64_t s = (next_random(&seed) * 32768 + next_random(&seed)) % 998999000;
            int64_t len = 1 + (next_random(&seed) * 32768 + next_random(&seed)) % 1000000;
            ls[d][i] = s;
            le[d][i] = s + len;
        }
    int64_t sum = 0;
    for (int64_t round = 0; round < 40; round++)
        for (int d = 0; d < 20; d++) {
            MyCalendarThree cal = {{NULL, 0, 0}, {NULL, 0, 0}};
            for (int i = 0; i < 1000; i++) sum += book(&cal, ls[d][i] + round, le[d][i] + round);
            free(cal.starts.items);
            free(cal.ends.items);
        }
    printf("40 rounds of 20 lists of 1000 bookings: answers sum %lld\n", (long long)sum);
    return 0;
}
