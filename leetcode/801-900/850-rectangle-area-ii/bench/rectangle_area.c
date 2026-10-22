// Benchmark for #850: Rectangle Area II -- C twin of the Kāra segment-tree
// arm (a sweep line over a segment tree).
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct { int64_t x, delta, y1, y2; } Event;

typedef struct {
    const int64_t *ys;
    int64_t *count;
    int64_t *length;
} Cover;

static void update(Cover *t, int64_t node, int64_t lo, int64_t hi, int64_t a, int64_t b, int64_t delta) {
    if (b <= lo || hi <= a) return;
    if (a <= lo && hi <= b) {
        t->count[node] += delta;
    } else {
        int64_t mid = (lo + hi) / 2;
        update(t, 2 * node, lo, mid, a, b, delta);
        update(t, 2 * node + 1, mid, hi, a, b, delta);
    }
    if (t->count[node] > 0) t->length[node] = t->ys[hi] - t->ys[lo];
    else if (hi - lo == 1) t->length[node] = 0;
    else t->length[node] = t->length[2 * node] + t->length[2 * node + 1];
}

static int cmp_i64(const void *p, const void *q) {
    int64_t a = *(const int64_t *)p, b = *(const int64_t *)q;
    return (a > b) - (a < b);
}

static int cmp_event(const void *p, const void *q) {
    const Event *a = p, *b = q;
    if (a->x != b->x) return (a->x > b->x) - (a->x < b->x);
    if (a->delta != b->delta) return (a->delta > b->delta) - (a->delta < b->delta);
    if (a->y1 != b->y1) return (a->y1 > b->y1) - (a->y1 < b->y1);
    return (a->y2 > b->y2) - (a->y2 < b->y2);
}

static int64_t find(const int64_t *ys, int64_t len, int64_t v) {
    int64_t lo = 0, hi = len;
    while (lo < hi) {
        int64_t mid = (lo + hi) / 2;
        if (ys[mid] < v) lo = mid + 1;
        else hi = mid;
    }
    return lo;
}

static int64_t rectangle_area(const int64_t (*rectangles)[4], int64_t n) {
    int64_t *ys = malloc(sizeof(int64_t) * 2 * n);
    Event *events = malloc(sizeof(Event) * 2 * n);
    for (int64_t i = 0; i < n; i++) {
        const int64_t *r = rectangles[i];
        ys[2 * i] = r[1];
        ys[2 * i + 1] = r[3];
        events[2 * i] = (Event){r[0], 1, r[1], r[3]};
        events[2 * i + 1] = (Event){r[2], -1, r[1], r[3]};
    }
    qsort(ys, 2 * n, sizeof(int64_t), cmp_i64);
    int64_t len = 0;
    for (int64_t i = 0; i < 2 * n; i++)
        if (len == 0 || ys[len - 1] != ys[i]) ys[len++] = ys[i];
    qsort(events, 2 * n, sizeof(Event), cmp_event);
    int64_t segments = len - 1;
    Cover t = {ys, calloc(4 * len, sizeof(int64_t)), calloc(4 * len, sizeof(int64_t))};
    int64_t area = 0, prev_x = 0;
    for (int64_t i = 0; i < 2 * n; i++) {
        Event e = events[i];
        area += t.length[1] * (e.x - prev_x);
        prev_x = e.x;
        if (segments > 0) update(&t, 1, 0, segments, find(ys, len, e.y1), find(ys, len, e.y2), e.delta);
    }
    free(t.count);
    free(t.length);
    free(events);
    free(ys);
    return area % 1000000007;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t count = 64, rounds = 8000, n = 200, limit = 1000000000;
    int64_t seed = 850;
    static int64_t sets[64][200][4];
    for (int64_t g = 0; g < count; g++) {
        int64_t size = limit >> (g % 8);
        for (int64_t i = 0; i < n; i++) {
            int64_t a = (next_random(&seed) * 32768 + next_random(&seed)) % (size + 1);
            int64_t b = (next_random(&seed) * 32768 + next_random(&seed)) % (size + 1);
            int64_t c = (next_random(&seed) * 32768 + next_random(&seed)) % (size + 1);
            int64_t d = (next_random(&seed) * 32768 + next_random(&seed)) % (size + 1);
            sets[g][i][0] = a < b ? a : b;
            sets[g][i][1] = c < d ? c : d;
            sets[g][i][2] = a < b ? b : a;
            sets[g][i][3] = c < d ? d : c;
        }
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t a = rectangle_area((const int64_t (*)[4])sets[round % count], n);
        total += a;
        checksum = (checksum * 31 + a) % 1000000007;
    }
    printf("%lld rounds of %lld sets: areas sum to %lld, checksum %lld\n", (long long)rounds, (long long)count,
           (long long)total, (long long)checksum);
    return 0;
}
