// Benchmark for #373 -- mirror of k_smallest_pairs.kara, with a hand-written
// min-heap of (sum, i, j) triples ordered as tuples.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { int64_t sum, i, j; } Front;

static int less(const Front *a, const Front *b) {
    if (a->sum != b->sum) return a->sum < b->sum;
    if (a->i != b->i) return a->i < b->i;
    return a->j < b->j;
}

static void push(Front *h, int64_t *n, Front f) {
    int64_t c = (*n)++;
    h[c] = f;
    while (c > 0) {
        int64_t p = (c - 1) / 2;
        if (!less(&h[c], &h[p])) break;
        Front t = h[c]; h[c] = h[p]; h[p] = t;
        c = p;
    }
}

static Front pop(Front *h, int64_t *n) {
    Front top = h[0];
    h[0] = h[--*n];
    int64_t c = 0;
    for (;;) {
        int64_t l = 2 * c + 1, r = l + 1, m = c;
        if (l < *n && less(&h[l], &h[m])) m = l;
        if (r < *n && less(&h[r], &h[m])) m = r;
        if (m == c) break;
        Front t = h[c]; h[c] = h[m]; h[m] = t;
        c = m;
    }
    return top;
}

// Writes up to k pairs into out_u/out_w and returns how many.
static int64_t k_smallest_pairs(const int64_t *nums1, int64_t n1, const int64_t *nums2, int64_t n2,
                                int64_t k, int64_t *out_u, int64_t *out_w) {
    int64_t count = 0;
    if (n1 == 0 || n2 == 0) return 0;
    int64_t rows = n1 < k ? n1 : k;
    Front *fronts = malloc(sizeof(Front) * (rows + 1));
    int64_t size = 0;
    for (int64_t i = 0; i < rows; i++) push(fronts, &size, (Front){nums1[i] + nums2[0], i, 0});
    while (count < k && size > 0) {
        Front f = pop(fronts, &size);
        out_u[count] = nums1[f.i];
        out_w[count] = nums2[f.j];
        count++;
        if (f.j + 1 < n2) push(fronts, &size, (Front){nums1[f.i] + nums2[f.j + 1], f.i, f.j + 1});
    }
    free(fronts);
    return count;
}

int main(void) {
    int64_t seed = 373, checksum = 0;
    static int64_t nums1[100000], nums2[100000], out_u[10000], out_w[10000];
    for (int round = 0; round < 20; round++) {
        int64_t v = -1000000000;
        for (int i = 0; i < 100000; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            v += (seed / 65536) % 20000;
            nums1[i] = v;
        }
        v = -1000000000;
        for (int i = 0; i < 100000; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            v += (seed / 65536) % 20000;
            nums2[i] = v;
        }
        int64_t n = k_smallest_pairs(nums1, 100000, nums2, 100000, 10000, out_u, out_w);
        for (int64_t p = 0; p < n; p++)
            checksum = (checksum * 31 + (out_u[p] + out_w[p]) % 1000000007 + 2000000000) % 1000000007;
    }
    printf("checksum %lld\n", (long long)checksum);
    return 0;
}
