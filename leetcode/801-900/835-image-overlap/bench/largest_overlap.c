// Benchmark for #835: Image Overlap -- the ★ arm (shifts counted over pairs of ones).
//
// Mirrors largest_overlap.kara: every pair of a one in the first image and
// a one in the second votes for the shift that lays the first on the
// second, and the shift with the most votes is the answer. As in the Kāra
// program, the lists of ones grow by doubling and the vote table is a
// fresh allocation per call.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 30

typedef struct {
    int64_t (*data)[2];
    int64_t len, cap;
} Cells;

static void push(Cells *v, int64_t r, int64_t c) {
    if (v->len == v->cap) {
        v->cap = v->cap ? v->cap * 2 : 4;
        v->data = realloc(v->data, (size_t)v->cap * sizeof(*v->data));
    }
    v->data[v->len][0] = r;
    v->data[v->len][1] = c;
    v->len++;
}

static int64_t largest_overlap(int64_t n, const int64_t img1[N][N], const int64_t img2[N][N]) {
    Cells ones1 = {0, 0, 0}, ones2 = {0, 0, 0};
    for (int64_t r = 0; r < n; r++) {
        for (int64_t c = 0; c < n; c++) {
            if (img1[r][c] == 1) push(&ones1, r, c);
            if (img2[r][c] == 1) push(&ones2, r, c);
        }
    }
    int64_t width = 2 * n - 1;
    int64_t *votes = calloc((size_t)(width * width), sizeof(int64_t));
    int64_t best = 0;
    for (int64_t i = 0; i < ones1.len; i++) {
        int64_t r1 = ones1.data[i][0], c1 = ones1.data[i][1];
        for (int64_t j = 0; j < ones2.len; j++) {
            int64_t r2 = ones2.data[j][0], c2 = ones2.data[j][1];
            int64_t k = (r2 - r1 + n - 1) * width + (c2 - c1 + n - 1);
            votes[k] += 1;
            if (votes[k] > best) best = votes[k];
        }
    }
    free(votes);
    free(ones1.data);
    free(ones2.data);
    return best;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    // 64 pairs of images drawn once, each of LeetCode's largest size, 30
    // by 30, the share of ones running from 2% to 98% over the pairs, the
    // two images of pair k at 2k and 2k + 1 in one list. Each round solves
    // the next pair.
    enum { COUNT = 64 };
    const int64_t rounds = 4000, n = N;
    int64_t seed = 835;
    static int64_t images[2 * COUNT][N][N];
    for (int64_t g = 0; g < COUNT; g++) {
        int64_t percent = 2 + g * 96 / (COUNT - 1);
        for (int64_t i = 0; i < 2; i++)
            for (int64_t r = 0; r < n; r++)
                for (int64_t c = 0; c < n; c++)
                    images[2 * g + i][r][c] = next_random(&seed) % 100 < percent ? 1 : 0;
    }
    int64_t total = 0, checksum = 0;
    for (int64_t round = 0; round < rounds; round++) {
        int64_t k = round % COUNT;
        int64_t x = largest_overlap(n, (const int64_t(*)[N])images[2 * k], (const int64_t(*)[N])images[2 * k + 1]);
        total += x;
        checksum = (checksum * 131 + x) % 1000000007;
    }
    printf("%lld rounds of %d pairs: overlaps total %lld, checksum %lld\n", (long long)rounds, COUNT,
           (long long)total, (long long)checksum);
    return 0;
}
