// LeetCode #1802: Maximum Value at a Given Index in a Bounded Array -- the
// bench in C: the ★ arm over 4000 random cases built once, 1000000 calls.
#include <stdint.h>
#include <stdio.h>

static int64_t side(int64_t v, int64_t k) {
    if (k <= v - 1) return (v - 1 + v - k) * k / 2;
    return (v - 1) * v / 2 + (k - (v - 1));
}

static int32_t max_value(int32_t n32, int32_t index32, int32_t max_sum32) {
    int64_t n = n32, index = index32, max_sum = max_sum32;
    int64_t lo = 1, hi = max_sum;
    while (lo < hi) {
        int64_t mid = (lo + hi + 1) / 2;
        if (mid + side(mid, index) + side(mid, n - 1 - index) <= max_sum) {
            lo = mid;
        } else {
            hi = mid - 1;
        }
    }
    return (int32_t)lo;
}

static int64_t seed = 1802;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int32_t cases[4000][3];
    for (int c = 0; c < 4000; c++) {
        int64_t n = 1 + next_random() % 1000000;
        int64_t index = next_random() % n;
        int64_t hi = next_random();
        int64_t wide = hi * 32768 + next_random();
        int64_t max_sum = n + wide % (1000000001 - n);
        cases[c][0] = (int32_t)n;
        cases[c][1] = (int32_t)index;
        cases[c][2] = (int32_t)max_sum;
    }
    int64_t check = 0;
    for (int64_t call = 0; call < 1000000; call++) {
        int32_t *c = cases[(check + call) % 4000];
        check = (check * 31 + max_value(c[0], c[1], c[2])) % 1000000007;
    }
    printf("1000000 calls over 4000 cases: checksum %lld\n", (long long)check);
    return 0;
}
