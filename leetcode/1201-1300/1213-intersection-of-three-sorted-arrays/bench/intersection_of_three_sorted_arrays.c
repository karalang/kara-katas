// LeetCode #1213 bench, in C: the ★ arm (three pointers, all three stepping
// on when the values agree and otherwise only those at the least value) on
// 1000 triples of arrays of 600 to 950 values drawn once, then 10 rounds
// over the triples, every answer's length and last value folded into a
// checksum.

#include <stdio.h>
#include <stdlib.h>

#define TRIPLES 1000

static long long seed = 1213;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

typedef struct {
    long long *v;
    int n;
} arr_t;

static arr_t random_sorted(long long percent) {
    arr_t a = {malloc(2000 * sizeof(long long)), 0};
    for (long long v = 1; v <= 2000; v++)
        if (next_random() % 100 < percent) a.v[a.n++] = v;
    return a;
}

// The answer is written to `out`; its length is returned.
static int arrays_intersection(arr_t x, arr_t y, arr_t z, long long *out) {
    int i = 0, j = 0, k = 0, m = 0;
    while (i < x.n && j < y.n && k < z.n) {
        long long a = x.v[i], b = y.v[j], c = z.v[k];
        if (a == b && b == c) {
            out[m++] = a;
            i++;
            j++;
            k++;
        } else {
            long long least = a < b ? a : b;
            if (c < least) least = c;
            if (a == least) i++;
            if (b == least) j++;
            if (c == least) k++;
        }
    }
    return m;
}

int main(void) {
    static arr_t triples[TRIPLES][3];
    for (int t = 0; t < TRIPLES; t++)
        for (int s = 0; s < 3; s++) triples[t][s] = random_sorted(33 + next_random() % 12);
    static long long out[2000];
    long long check = 0;
    for (int round = 0; round < 10; round++)
        for (int t = 0; t < TRIPLES; t++) {
            int m = arrays_intersection(triples[t][0], triples[t][1], triples[t][2], out);
            long long last = m > 0 ? out[m - 1] : 0;
            check = (check * 131 + m + last + round) % 1000000007;
        }
    printf("10 rounds over 1000 triples of 600 to 950 values: checksum %lld\n", check);
    return 0;
}
