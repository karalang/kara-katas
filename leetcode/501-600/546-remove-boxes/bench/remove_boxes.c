// Benchmark for #546: C mirror of the ★ arm (memoized, with the boxes
// carried along); see remove_boxes.kara. The memo is a fresh n * n * n
// array per call, as the Kāra one is.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t best(const int64_t *boxes, int64_t n, int64_t l, int64_t r, int64_t k,
                    int64_t *memo) {
    if (l > r) return 0;
    int64_t key = (l * n + r) * n + k;
    if (memo[key] >= 0) return memo[key];
    int64_t i = l, run = k + 1;
    while (i < r && boxes[i + 1] == boxes[l]) {
        i++;
        run++;
    }
    int64_t most = run * run + best(boxes, n, i + 1, r, 0, memo);
    for (int64_t m = i + 2; m <= r; m++) {
        if (boxes[m] == boxes[l] && boxes[m - 1] != boxes[l]) {
            int64_t v = best(boxes, n, i + 1, m - 1, 0, memo) + best(boxes, n, m, r, run, memo);
            if (v > most) most = v;
        }
    }
    memo[key] = most;
    return most;
}

static int64_t remove_boxes(const int64_t *boxes, int64_t n) {
    int64_t *memo = malloc(n * n * n * sizeof(int64_t));
    for (int64_t i = 0; i < n * n * n; i++) memo[i] = -1;
    int64_t out = best(boxes, n, 0, n - 1, 0, memo);
    free(memo);
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    // 40 random rows of 100 boxes (the problem's most), from 2 to 9
    // colours by the row, built once. Then 5 times over every row is
    // answered and the points go into the checksum.
    int64_t rows = 40, seed = 546;
    int64_t all[40][100];
    for (int64_t g = 0; g < rows; g++) {
        int64_t colours = 2 + g % 8;
        for (int i = 0; i < 100; i++) all[g][i] = 1 + next_random(&seed) % colours;
    }
    int64_t total = 0, checksum = 0;
    for (int round = 0; round < 5; round++) {
        for (int64_t t = 0; t < rows; t++) {
            int64_t points = remove_boxes(all[t], 100);
            total += points;
            checksum = (checksum * 31 + points) % 1000000007;
        }
    }
    printf("%lld rows, 5 times each: %lld points, checksum %lld\n", (long long)rows,
           (long long)total, (long long)checksum);
    return 0;
}
