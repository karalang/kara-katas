// Benchmark mirror of LeetCode #321 — same split-shrink-merge as
// bench/create_max_number.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define LEN1 1500
#define LEN2 1700
#define PASSES 24
#define MODULUS 1073741789LL

static int64_t next(int64_t *seed) {
    *seed = (*seed * 1103515245LL + 12345LL) % 2147483648LL;
    return *seed / 65536;
}

static void shrink(const int64_t *nums, int64_t len, int64_t keep, int64_t *out) {
    int64_t top = 0;
    int64_t drop = len - keep;
    for (int64_t i = 0; i < len; i++) {
        int64_t d = nums[i];
        while (drop > 0 && top > 0 && out[top - 1] < d) {
            top--;
            drop--;
        }
        if (top < keep) {
            out[top++] = d;
        } else {
            drop--;
        }
    }
}

static int suffix_greater(const int64_t *a, int64_t alen, int64_t i,
                          const int64_t *b, int64_t blen, int64_t j) {
    int64_t x = i, y = j;
    while (x < alen && y < blen && a[x] == b[y]) {
        x++;
        y++;
    }
    if (y == blen) return x < alen;
    if (x == alen) return 0;
    return a[x] > b[y];
}

static void merge(const int64_t *a, int64_t alen, const int64_t *b, int64_t blen, int64_t *out) {
    int64_t i = 0, j = 0, t = 0;
    while (i < alen || j < blen) {
        if (suffix_greater(a, alen, i, b, blen, j)) {
            out[t] = a[i++];
        } else {
            out[t] = b[j++];
        }
        t++;
    }
}

int main(void) {
    int64_t seed = 321;
    int64_t sink = 0;
    int64_t digits_out = 0;

    int64_t *left = calloc(LEN1 + LEN2, sizeof(int64_t));
    int64_t *right = calloc(LEN1 + LEN2, sizeof(int64_t));
    int64_t *cand = calloc(LEN1 + LEN2, sizeof(int64_t));
    int64_t *best = calloc(LEN1 + LEN2, sizeof(int64_t));
    int64_t *nums1 = calloc(LEN1, sizeof(int64_t));
    int64_t *nums2 = calloc(LEN2, sizeof(int64_t));

    for (int64_t p = 0; p < PASSES; p++) {
        for (int64_t x = 0; x < LEN1; x++) nums1[x] = next(&seed) % 10;
        for (int64_t x = 0; x < LEN2; x++) nums2[x] = next(&seed) % 10;

        int64_t ks[3] = {LEN1 / 3, (LEN1 + LEN2) / 2, LEN1 + LEN2 - 7 * (p + 1)};
        for (int t = 0; t < 3; t++) {
            int64_t k = ks[t];
            int64_t lo = k - LEN2;
            if (lo < 0) lo = 0;
            int64_t hi = k;
            if (hi > LEN1) hi = LEN1;
            int have = 0;
            for (int64_t i = lo; i <= hi; i++) {
                shrink(nums1, LEN1, i, left);
                shrink(nums2, LEN2, k - i, right);
                merge(left, i, right, k - i, cand);
                if (!have || suffix_greater(cand, k, 0, best, k, 0)) {
                    for (int64_t x = 0; x < k; x++) best[x] = cand[x];
                    have = 1;
                }
            }

            int64_t acc = 0;
            for (int64_t x = 0; x < k; x++) acc = (acc * 131 + best[x] + 1) % MODULUS;
            sink = (sink * 1000003 + acc) % MODULUS;
            digits_out += k;
        }
    }

    printf("sink %lld digits %lld\n", (long long)sink, (long long)digits_out);
    free(left);
    free(right);
    free(cand);
    free(best);
    free(nums1);
    free(nums2);
    return 0;
}
