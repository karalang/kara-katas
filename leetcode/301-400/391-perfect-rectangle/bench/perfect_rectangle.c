// Benchmark for #391: mirror of perfect_rectangle.kara (corners and area).
// C has no set type, so the corner set is an open-addressing hash set of
// (x, y) pairs with linear probing and backward-shift deletion.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int64_t x, y; uint8_t used; } Slot;
typedef struct { Slot *slots; size_t cap, len; } Set;

static uint64_t hash(int64_t x, int64_t y) {
    uint64_t h = (uint64_t)x * 0x9E3779B97F4A7C15ULL ^ (uint64_t)y * 0xC2B2AE3D27D4EB4FULL;
    return h ^ (h >> 29);
}

static void set_init(Set *s, size_t cap) {
    s->cap = cap;
    s->len = 0;
    s->slots = calloc(cap, sizeof(Slot));
}

static size_t set_find(const Set *s, int64_t x, int64_t y) {
    size_t i = hash(x, y) & (s->cap - 1);
    while (s->slots[i].used && !(s->slots[i].x == x && s->slots[i].y == y)) {
        i = (i + 1) & (s->cap - 1);
    }
    return i;
}

static int set_contains(const Set *s, int64_t x, int64_t y) {
    return s->slots[set_find(s, x, y)].used;
}

static void set_grow(Set *s);

static void set_insert(Set *s, int64_t x, int64_t y) {
    if ((s->len + 1) * 2 > s->cap) {
        set_grow(s);
    }
    size_t i = set_find(s, x, y);
    if (!s->slots[i].used) {
        s->slots[i] = (Slot){x, y, 1};
        s->len++;
    }
}

static void set_grow(Set *s) {
    Set bigger;
    set_init(&bigger, s->cap * 2);
    for (size_t i = 0; i < s->cap; i++) {
        if (s->slots[i].used) {
            set_insert(&bigger, s->slots[i].x, s->slots[i].y);
        }
    }
    free(s->slots);
    *s = bigger;
}

// Removes (x, y) and returns 1 if it was present.
static int set_remove(Set *s, int64_t x, int64_t y) {
    size_t i = set_find(s, x, y);
    if (!s->slots[i].used) {
        return 0;
    }
    s->slots[i].used = 0;
    s->len--;
    size_t j = i;
    for (;;) {
        j = (j + 1) & (s->cap - 1);
        if (!s->slots[j].used) {
            break;
        }
        size_t home = hash(s->slots[j].x, s->slots[j].y) & (s->cap - 1);
        // Move j back into the hole at i unless its home lies cyclically in (i, j].
        int stays = (i <= j) ? (i < home && home <= j) : (i < home || home <= j);
        if (!stays) {
            s->slots[i] = s->slots[j];
            s->slots[j].used = 0;
            i = j;
        }
    }
    return 1;
}

typedef struct { int64_t v[4]; } Rect;

static int is_rectangle_cover(const Rect *rects, size_t n) {
    int64_t min_x = rects[0].v[0], min_y = rects[0].v[1];
    int64_t max_x = rects[0].v[2], max_y = rects[0].v[3];
    int64_t area = 0;
    Set corners;
    set_init(&corners, 16);
    for (size_t k = 0; k < n; k++) {
        const int64_t *r = rects[k].v;
        if (r[0] < min_x) min_x = r[0];
        if (r[1] < min_y) min_y = r[1];
        if (r[2] > max_x) max_x = r[2];
        if (r[3] > max_y) max_y = r[3];
        area += (r[2] - r[0]) * (r[3] - r[1]);
        int64_t ps[4][2] = {{r[0], r[1]}, {r[0], r[3]}, {r[2], r[1]}, {r[2], r[3]}};
        for (int q = 0; q < 4; q++) {
            if (!set_remove(&corners, ps[q][0], ps[q][1])) {
                set_insert(&corners, ps[q][0], ps[q][1]);
            }
        }
    }
    int ok = area == (max_x - min_x) * (max_y - min_y)
        && corners.len == 4
        && set_contains(&corners, min_x, min_y)
        && set_contains(&corners, min_x, max_y)
        && set_contains(&corners, max_x, min_y)
        && set_contains(&corners, max_x, max_y);
    free(corners.slots);
    return ok;
}

static int64_t seed = 391;

static int64_t step(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t big(void) {
    int64_t hi = step();
    return hi * 32768 + step();
}

typedef struct { Rect *r; size_t len, cap; } Rects;

static void push(Rects *out, int64_t x1, int64_t y1, int64_t x2, int64_t y2) {
    if (out->len == out->cap) {
        out->cap = out->cap ? out->cap * 2 : 16;
        out->r = realloc(out->r, out->cap * sizeof(Rect));
    }
    out->r[out->len++] = (Rect){{x1, y1, x2, y2}};
}

static void tile(int64_t x1, int64_t y1, int64_t x2, int64_t y2, int64_t pieces, Rects *out) {
    int64_t w = x2 - x1, h = y2 - y1;
    if (pieces <= 1 || (w < 2 && h < 2)) {
        push(out, x1, y1, x2, y2);
        return;
    }
    int64_t left = 1 + step() % (pieces - 1);
    int across = w < 2 ? 0 : h < 2 ? 1 : step() % 2 == 0;
    if (across) {
        int64_t cut = x1 + 1 + big() % (w - 1);
        tile(x1, y1, cut, y2, left, out);
        tile(cut, y1, x2, y2, pieces - left, out);
    } else {
        int64_t cut = y1 + 1 + big() % (h - 1);
        tile(x1, y1, x2, cut, left, out);
        tile(x1, cut, x2, y2, pieces - left, out);
    }
}

int main(void) {
    Rects tilings[50];
    memset(tilings, 0, sizeof tilings);
    for (int i = 0; i < 50; i++) {
        tile(0, 0, 100000, 100000, 20000, &tilings[i]);
    }
    int perfect = 0;
    int64_t checksum = 0;
    for (int round = 0; round < 300; round++) {
        Rects *t = &tilings[round % 50];
        size_t at = (size_t)(big() % (int64_t)t->len);
        int64_t edit = step() % 3;
        int64_t *r = t->r[at].v;
        if (edit == 1) {
            r[0] += 1;
            r[2] += 1;
        } else if (edit == 2) {
            r[3] += 1;
        }
        int ok = is_rectangle_cover(t->r, t->len);
        if (edit == 1) {
            r[0] -= 1;
            r[2] -= 1;
        } else if (edit == 2) {
            r[3] -= 1;
        }
        if (ok) {
            perfect++;
        }
        checksum = (checksum * 3 + (ok ? 1 : 2)) % 1000000007;
    }
    printf("300 rounds over 50 tilings of 20000 pieces: %d perfect, checksum %lld\n", perfect, (long long)checksum);
    return 0;
}
