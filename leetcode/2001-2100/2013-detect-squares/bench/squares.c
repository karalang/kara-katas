// LeetCode #2013: Detect Squares -- the ★ arm's benchmark, a mirror of
// squares.kara.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct { int64_t x, y; } Point;

typedef struct {
    int64_t *rows[1001];
    Point *points;
    size_t len, cap;
} DetectSquares;

static void ds_init(DetectSquares *s) {
    for (int i = 0; i < 1001; i++) s->rows[i] = NULL;
    s->points = NULL;
    s->len = s->cap = 0;
}

static void ds_free(DetectSquares *s) {
    for (int i = 0; i < 1001; i++) free(s->rows[i]);
    free(s->points);
}

static int64_t ds_at(const DetectSquares *s, int64_t x, int64_t y) {
    return s->rows[x] ? s->rows[x][y] : 0;
}

static void ds_add(DetectSquares *s, Point p) {
    if (!s->rows[p.x]) s->rows[p.x] = calloc(1001, sizeof(int64_t));
    if (s->rows[p.x][p.y] == 0) {
        if (s->len == s->cap) {
            s->cap = s->cap ? s->cap * 2 : 4;
            s->points = realloc(s->points, s->cap * sizeof(Point));
        }
        s->points[s->len++] = p;
    }
    s->rows[p.x][p.y] += 1;
}

static int64_t ds_count(const DetectSquares *s, Point p) {
    int64_t ways = 0;
    for (size_t i = 0; i < s->len; i++) {
        int64_t px = s->points[i].x, py = s->points[i].y;
        int64_t dx = px - p.x, dy = py - p.y;
        if (px != p.x && llabs(dx) == llabs(dy))
            ways += ds_at(s, px, py) * ds_at(s, p.x, py) * ds_at(s, px, p.y);
    }
    return ways;
}

static int64_t seed = 2013;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t calls = 0, sum = 0, check = 0;
    for (int64_t r = 0; r < 20; r++) {
        DetectSquares s;
        ds_init(&s);
        for (int i = 0; i < 20000; i++) {
            int64_t base = (r % 10) * 90;
            Point p;
            p.x = base + next_random() % 60;
            p.y = base + next_random() % 60;
            if (next_random() % 3 == 0) {
                int64_t ways = ds_count(&s, p);
                calls++;
                sum += ways;
                check = (check * 31 + ways) % 1000000007;
            } else {
                ds_add(&s, p);
            }
        }
        ds_free(&s);
    }
    printf("%lld counts: sum %lld, checksum %lld\n", (long long)calls, (long long)sum, (long long)check);
    return 0;
}
