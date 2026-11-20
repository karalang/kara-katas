// LeetCode #1272 bench, in C: the ★ arm (one pass; an interval the cut
// misses kept whole, one it meets keeping its parts before and after) on 20
// random lists of 10,000 intervals drawn once, each cut three ways, 40
// rounds; every interval kept folded into a checksum. Each interval is its
// own two-element array, as LeetCode's `int[][]` is.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t *pair(int64_t a, int64_t b) {
    int64_t *p = malloc(2 * sizeof(int64_t));
    p[0] = a;
    p[1] = b;
    return p;
}

// Returns the kept intervals, `*count` of them; the caller frees them.
static int64_t **remove_interval(int64_t **intervals, int n, int64_t lo, int64_t hi, int *count) {
    int64_t **out = malloc((n + 1) * sizeof(int64_t *));
    int k = 0;
    for (int i = 0; i < n; i++) {
        int64_t a = intervals[i][0], b = intervals[i][1];
        if (b <= lo || a >= hi) {
            out[k++] = pair(a, b);
            continue;
        }
        if (a < lo) out[k++] = pair(a, lo);
        if (b > hi) out[k++] = pair(hi, b);
    }
    *count = k;
    return out;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    int64_t seed = 1272;
    int64_t **lists[20];
    for (int l = 0; l < 20; l++) {
        lists[l] = malloc(10000 * sizeof(int64_t *));
        int64_t at = -1000000;
        for (int i = 0; i < 10000; i++) {
            int64_t a = at + next_random(&seed) % 50;
            int64_t b = a + 1 + next_random(&seed) % 50;
            lists[l][i] = pair(a, b);
            at = b;
        }
    }
    static const int64_t cuts[3][2] = {{-990000, -800000}, {-700000, -699990}, {-1000000, 1000000}};
    int64_t check = 0;
    for (int64_t round = 0; round < 40; round++)
        for (int l = 0; l < 20; l++)
            for (int c = 0; c < 3; c++) {
                int count;
                int64_t **kept = remove_interval(lists[l], 10000, cuts[c][0], cuts[c][1], &count);
                check = (check * 131 + count + round) % 1000000007;
                for (int i = 0; i < count; i++) {
                    check = (check * 131 + kept[i][0] + kept[i][1] + 2000000) % 1000000007;
                    free(kept[i]);
                }
                free(kept);
            }
    printf("40 rounds of 20 lists cut 3 ways: checksum %lld\n", (long long)check);
    return 0;
}
