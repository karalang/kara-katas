// LeetCode #2286: Booking Concert Tickets in Groups -- the bench, the ★
// arm's C twin. A segment tree of each range's largest free run and free
// total; a gather answers through two out-parameters.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t seats, size;
    int64_t *most, *free;
} Show;

static int64_t max64(int64_t a, int64_t b) { return a > b ? a : b; }

static void show_new(Show *s, int64_t n, int64_t m) {
    int64_t size = 1;
    while (size < n) size *= 2;
    s->seats = m;
    s->size = size;
    s->most = calloc((size_t)(2 * size), sizeof(int64_t));
    s->free = calloc((size_t)(2 * size), sizeof(int64_t));
    for (int64_t r = 0; r < n; r++) s->most[size + r] = s->free[size + r] = m;
    for (int64_t p = size - 1; p >= 1; p--) {
        s->most[p] = max64(s->most[2 * p], s->most[2 * p + 1]);
        s->free[p] = s->free[2 * p] + s->free[2 * p + 1];
    }
}

static void show_free(Show *s) {
    free(s->most);
    free(s->free);
}

static void set(Show *s, int64_t row, int64_t left) {
    int64_t p = s->size + row;
    s->most[p] = s->free[p] = left;
    for (p /= 2; p >= 1; p /= 2) {
        s->most[p] = max64(s->most[2 * p], s->most[2 * p + 1]);
        s->free[p] = s->free[2 * p] + s->free[2 * p + 1];
    }
}

static int64_t leftmost(const Show *s, int64_t k) {
    if (s->most[1] < k) return -1;
    int64_t p = 1;
    while (p < s->size) p = s->most[2 * p] >= k ? 2 * p : 2 * p + 1;
    return p - s->size;
}

static int64_t free_through(const Show *s, int64_t row) {
    int64_t total = 0, lo = s->size, hi = s->size + row + 1;
    while (lo < hi) {
        if (lo % 2 == 1) total += s->free[lo++];
        if (hi % 2 == 1) total += s->free[--hi];
        lo /= 2;
        hi /= 2;
    }
    return total;
}

static bool gather(Show *s, int64_t k, int64_t max_row, int64_t *row_out, int64_t *seat_out) {
    int64_t row = leftmost(s, k);
    if (row < 0 || row > max_row) return false;
    int64_t left = s->free[s->size + row];
    set(s, row, left - k);
    *row_out = row;
    *seat_out = s->seats - left;
    return true;
}

static bool scatter(Show *s, int64_t k, int64_t max_row) {
    if (free_through(s, max_row) < k) return false;
    int64_t need = k;
    while (need > 0) {
        int64_t row = leftmost(s, 1);
        int64_t left = s->free[s->size + row];
        int64_t take = left < need ? left : need;
        set(s, row, left - take);
        need -= take;
    }
    return true;
}

// ---- bench harness ---------------------------------------------------------

static int64_t seed = 2286;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    static bool kind[50000];
    static int64_t ks[50000], rows[50000];
    for (int i = 0; i < 50000; i++) {
        ks[i] = wide_random() % 1000000000 + 1;
        rows[i] = wide_random() % 50000;
        kind[i] = next_random() % 2 == 0;
    }
    int64_t check = 0;
    for (int t = 0; t < 40; t++) {
        Show s;
        show_new(&s, 50000, 1000000000);
        for (int i = 0; i < 50000; i++) {
            int64_t mark, r, c;
            if (kind[i]) {
                mark = gather(&s, ks[i], rows[i], &r, &c) ? (r * 1000003 + c) % 1000000007 + 3 : 0;
            } else {
                mark = scatter(&s, ks[i], rows[i]) ? 1 : 2;
            }
            check = (check * 31 + mark) % 1000000007;
        }
        show_free(&s);
    }
    printf("40 shows of 50000 calls: checksum %lld\n", (long long)check);
    return 0;
}
