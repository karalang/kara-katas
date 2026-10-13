// Benchmark for #497: C mirror of the ★ arm (prefix sums); see
// random_point_rects.kara. Each solution gets its own copy of the
// rectangles, as the ★ arm's does.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SETS 500
#define RECTS 100
#define PICKS 10000

typedef struct {
    int64_t seed;
} Draw;

static int64_t step(Draw *d) {
    d->seed = (d->seed * 1103515245 + 12345) % 2147483648LL;
    return d->seed / 65536;
}

// Uniform in [0, n) for n up to 2^30: 30 random bits, drawn again when
// they land in the last, incomplete run of n.
static int64_t below(Draw *d, int64_t n) {
    int64_t limit = 1073741824LL / n * n;
    for (;;) {
        int64_t high = step(d);
        int64_t low = step(d);
        int64_t r = high * 32768 + low;
        if (r < limit) {
            return r % n;
        }
    }
}

typedef struct {
    int64_t (*rects)[4];
    int64_t *ends;
    int64_t n;
    Draw draw;
} Solution;

static Solution solution_new(const int64_t (*rects)[4], int64_t n, int64_t seed) {
    Solution s;
    s.rects = malloc(n * sizeof(*s.rects));
    memcpy(s.rects, rects, n * sizeof(*s.rects));
    s.ends = malloc(n * sizeof(int64_t));
    s.n = n;
    int64_t total = 0;
    for (int64_t i = 0; i < n; i++) {
        total += (rects[i][2] - rects[i][0] + 1) * (rects[i][3] - rects[i][1] + 1);
        s.ends[i] = total;
    }
    s.draw.seed = seed;
    return s;
}

static void solution_free(Solution *s) {
    free(s->rects);
    free(s->ends);
}

static void pick(Solution *s, int64_t out[2]) {
    int64_t k = below(&s->draw, s->ends[s->n - 1]);
    int64_t low = 0, high = s->n - 1;
    while (low < high) {
        int64_t mid = (low + high) / 2;
        if (s->ends[mid] > k) {
            high = mid;
        } else {
            low = mid + 1;
        }
    }
    const int64_t *r = s->rects[low];
    int64_t before = low == 0 ? 0 : s->ends[low - 1];
    int64_t at = k - before;
    int64_t width = r[2] - r[0] + 1;
    out[0] = r[0] + at % width;
    out[1] = r[1] + at / width;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // 500 sets of 100 rectangles (the problem's most) of 1 to 2,001 on a
    // side, spread across the whole range, built once. Then each set gets
    // a fresh solution and 10,000 picks (the problem's most).
    static int64_t all[SETS][RECTS][4];
    int64_t seed = 497;
    for (int c = 0; c < SETS; c++) {
        for (int64_t i = 0; i < RECTS; i++) {
            int64_t x = -1000000000LL + i * 19000000 + next_random(&seed) % 1000;
            int64_t y = next_random(&seed) % 30000 * 60000 - 999000000LL;
            int64_t w = 1 + next_random(&seed) % 2001;
            int64_t h = 1 + next_random(&seed) % 2001;
            all[c][i][0] = x;
            all[c][i][1] = y;
            all[c][i][2] = x + w - 1;
            all[c][i][3] = y + h - 1;
        }
    }
    int64_t sum = 0, checksum = 0;
    for (int k = 0; k < SETS; k++) {
        Solution s = solution_new((const int64_t (*)[4])all[k], RECTS, k);
        for (int j = 0; j < PICKS; j++) {
            // Moved up by 10^9 so that every coordinate is at least 0.
            int64_t p[2];
            pick(&s, p);
            int64_t x = p[0] + 1000000000;
            int64_t y = p[1] + 1000000000;
            sum += x % 1000 + y % 1000;
            checksum = (checksum * 31 + x + 2 * y) % 1000000007;
        }
        solution_free(&s);
    }
    printf("%d sets of 100, 10000 picks each: sum of last three digits %lld, checksum %lld\n", SETS, (long long)sum, (long long)checksum);
    return 0;
}
