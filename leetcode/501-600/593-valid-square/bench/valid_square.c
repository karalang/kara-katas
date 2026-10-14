// Benchmark for #593: C mirror of the ★ arm (the six distances, sorted);
// see valid_square.kara. The distances go into an array on the stack,
// sorted by insertion.
#include <stdint.h>
#include <stdio.h>

static int64_t dist(const int64_t *a, const int64_t *b) {
    int64_t dx = a[0] - b[0], dy = a[1] - b[1];
    return dx * dx + dy * dy;
}

static int valid_square(const int64_t *p1, const int64_t *p2, const int64_t *p3, const int64_t *p4) {
    int64_t d[6] = {dist(p1, p2), dist(p1, p3), dist(p1, p4), dist(p2, p3), dist(p2, p4), dist(p3, p4)};
    for (int i = 1; i < 6; i++) {
        int64_t v = d[i];
        int j = i;
        while (j > 0 && d[j - 1] > v) {
            d[j] = d[j - 1];
            j--;
        }
        d[j] = v;
    }
    return d[0] > 0 && d[0] == d[3] && d[4] == d[5] && d[4] == 2 * d[0];
}

// ---- benchmark --------------------------------------------------------------

static int64_t step(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

static void random_points(int64_t *seed, int64_t p[4][2]) {
    int64_t kind = step(seed) % 3;
    if (kind == 2) {
        for (int k = 0; k < 4; k++) {
            p[k][0] = step(seed) % 7 - 3;
            p[k][1] = step(seed) % 7 - 3;
        }
        return;
    }
    int64_t x = step(seed) % 2001 - 1000;
    int64_t y = step(seed) % 2001 - 1000;
    int64_t dx = step(seed) % 41 - 20;
    int64_t dy = step(seed) % 41 - 20;
    if (dx == 0 && dy == 0)
        dx = 1;
    int64_t q[4][2] = {{x, y}, {x + dx, y + dy}, {x + dx - dy, y + dy + dx}, {x - dy, y + dx}};
    for (int k = 0; k < 4; k++) {
        p[k][0] = q[k][0];
        p[k][1] = q[k][1];
    }
    if (kind == 1) {
        int64_t k = step(seed) % 4;
        int64_t c = step(seed) % 2;
        p[k][c] += step(seed) % 2 == 0 ? 1 : -1;
    }
    for (int64_t k = 0; k < 3; k++) {
        int64_t j = k + step(seed) % (4 - k);
        int64_t t0 = p[k][0], t1 = p[k][1];
        p[k][0] = p[j][0];
        p[k][1] = p[j][1];
        p[j][0] = t0;
        p[j][1] = t1;
    }
}

int main(void) {
    enum { COUNT = 1000, ROUNDS = 20000 };
    int64_t seed = 593;
    static int64_t cases[COUNT][4][2];
    for (int k = 0; k < COUNT; k++)
        random_points(&seed, cases[k]);
    int64_t squares = 0, checksum = 0;
    for (int round = 0; round < ROUNDS; round++)
        for (int g = 0; g < COUNT; g++) {
            int64_t (*p)[2] = cases[(round * 7 + g) % COUNT];
            if (valid_square(p[0], p[1], p[2], p[3])) {
                squares++;
                checksum = (checksum * 31 + g + 1) % 1000000007;
            }
        }
    printf("%d cases, %d rounds: %lld squares, checksum %lld\n", COUNT, ROUNDS, (long long)squares,
           (long long)checksum);
    return 0;
}
