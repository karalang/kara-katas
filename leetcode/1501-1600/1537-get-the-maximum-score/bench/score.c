// LeetCode #1537: Get the Maximum Score -- bench: the ★ arm over 100
// random pairs of arrays built from 100000 values each, steps up to 50,
// built once and answered 20 times. C mirror of score.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t max_sum(const int64_t *nums1, int64_t n, const int64_t *nums2, int64_t m) {
    int64_t i = 0, j = 0, a = 0, b = 0;
    while (i < n || j < m) {
        if (i < n && (j == m || nums1[i] < nums2[j])) {
            a += nums1[i++];
        } else if (j < m && (i == n || nums2[j] < nums1[i])) {
            b += nums2[j++];
        } else {
            int64_t best = (a > b ? a : b) + nums1[i];
            a = best;
            b = best;
            i++;
            j++;
        }
    }
    return (a > b ? a : b) % 1000000007;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

typedef struct {
    int64_t *first, *second;
    int64_t n, m;
} Pair;

static Pair arrays(int64_t count, int64_t gap, int64_t *seed) {
    Pair p = {malloc((count + 1) * sizeof(int64_t)), malloc((count + 1) * sizeof(int64_t)), 0, 0};
    int64_t value = 0;
    int64_t both = next_random(seed) % 30 + 1;
    for (int64_t k = 0; k < count; k++) {
        value += next_random(seed) % gap + 1;
        int64_t roll = next_random(seed) % 100;
        if (roll < both) {
            p.first[p.n++] = value;
            p.second[p.m++] = value;
        } else if (roll < 50 + both / 2) {
            p.first[p.n++] = value;
        } else {
            p.second[p.m++] = value;
        }
    }
    if (p.n == 0) {
        p.first[p.n++] = value + 1;
    }
    if (p.m == 0) {
        p.second[p.m++] = value + 2;
    }
    return p;
}

int main(void) {
    int64_t seed = 1537;
    Pair pairs[100];
    for (int k = 0; k < 100; k++) {
        pairs[k] = arrays(100000, 50, &seed);
    }
    int64_t check = 0;
    for (int pass = 0; pass < 20; pass++) {
        for (int k = 0; k < 100; k++) {
            check = mix(check, max_sum(pairs[k].first, pairs[k].n, pairs[k].second, pairs[k].m));
        }
    }
    for (int k = 0; k < 100; k++) {
        free(pairs[k].first);
        free(pairs[k].second);
    }
    printf("20 passes over 100 pairs of 100000 values: checksum %lld\n", (long long)check);
    return 0;
}
