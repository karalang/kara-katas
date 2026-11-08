// LeetCode #2015: Average Height of Buildings in Each Segment -- the ★ arm's
// benchmark, a mirror of average.kara. The events are sorted with qsort on
// the same (position, height change, count change) order.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct { int64_t a, b, c; } Triple;

static int cmp_triple(const void *x, const void *y) {
    const Triple *p = x, *q = y;
    if (p->a != q->a) return p->a < q->a ? -1 : 1;
    if (p->b != q->b) return p->b < q->b ? -1 : 1;
    if (p->c != q->c) return p->c < q->c ? -1 : 1;
    return 0;
}

// fills `street` (room for 2n) and returns its length
static size_t average_height_of_buildings(const Triple *buildings, size_t n, Triple *street) {
    Triple *events = malloc(2 * n * sizeof(Triple));
    for (size_t k = 0; k < n; k++) {
        events[2 * k] = (Triple){buildings[k].a, buildings[k].c, 1};
        events[2 * k + 1] = (Triple){buildings[k].b, -buildings[k].c, -1};
    }
    qsort(events, 2 * n, sizeof(Triple), cmp_triple);
    size_t len = 0, i = 0, m = 2 * n;
    int64_t sum = 0, count = 0;
    while (i < m) {
        int64_t at = events[i].a;
        while (i < m && events[i].a == at) {
            sum += events[i].b;
            count += events[i].c;
            i++;
        }
        if (count == 0) continue;
        int64_t next = events[i].a;
        int64_t average = sum / count;
        if (len > 0 && street[len - 1].b == at && street[len - 1].c == average) {
            street[len - 1].b = next;
        } else {
            street[len++] = (Triple){at, next, average};
        }
    }
    free(events);
    return len;
}

static int64_t seed = 2015;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    enum { STREETS = 60, N = 10000 };
    Triple *streets = malloc(STREETS * N * sizeof(Triple));
    for (int s = 0; s < STREETS; s++) {
        for (int k = 0; k < N; k++) {
            int64_t a = next_random();
            int64_t start = (a * 32768 + next_random()) % 1000000;
            int64_t end = start + next_random() % (100 * (s + 1)) + 1;
            int64_t height = next_random() % (s + 2) + 1;
            streets[s * N + k] = (Triple){start, end, height};
        }
    }
    int64_t calls = 0, segments = 0, check = 0;
    for (int r = 0; r < 5; r++) {
        for (int s = 0; s < STREETS; s++) {
            Triple *street = malloc(2 * N * sizeof(Triple));
            size_t len = average_height_of_buildings(streets + s * N, N, street);
            calls++;
            segments += (int64_t)len;
            for (size_t k = 0; k < len; k++)
                check = (check * 31 + street[k].a + street[k].b * 7 + street[k].c * 13) % 1000000007;
            free(street);
        }
    }
    free(streets);
    printf("%lld calls: %lld segments, checksum %lld\n", (long long)calls, (long long)segments, (long long)check);
    return 0;
}
