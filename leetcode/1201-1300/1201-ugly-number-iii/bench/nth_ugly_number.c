// LeetCode #1201 bench: the ★ arm in C, over the same 50000 queries and
// 10 rounds as the Kāra bench.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t gcd(int64_t a, int64_t b) { return b == 0 ? a : gcd(b, a % b); }

static int64_t lcm(int64_t a, int64_t b) { return a / gcd(a, b) * b; }

static int64_t min64(int64_t a, int64_t b) { return a < b ? a : b; }

static int64_t nth_ugly_number(int64_t n, int64_t a, int64_t b, int64_t c) {
    int64_t ab = lcm(a, b), bc = lcm(b, c), ac = lcm(a, c);
    int64_t abc = lcm(ab, c);
    int64_t low = 1, high = n * min64(min64(a, b), c);
    while (low < high) {
        int64_t mid = low + (high - low) / 2;
        int64_t count = mid / a + mid / b + mid / c - mid / ab - mid / bc - mid / ac + mid / abc;
        if (count >= n) {
            high = mid;
        } else {
            low = mid + 1;
        }
    }
    return low;
}

static int64_t seed = 1201;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t big(void) {
    int64_t high = next_random();
    int64_t low = next_random();
    return high * 32768 + low;
}

int main(void) {
    const int64_t tops[3] = {1000000, 1000, 30};
    enum { Q = 50000 };
    int64_t (*queries)[4] = malloc(Q * sizeof *queries);
    for (int k = 0; k < Q; k++) {
        int64_t top = tops[k % 3];
        int64_t a = big() % top + 1;
        int64_t b = big() % top + 1;
        int64_t c = big() % top + 1;
        int64_t most = min64(2000000000 / min64(min64(a, b), c), 1000000000);
        int64_t n = big() % most + 1;
        queries[k][0] = n;
        queries[k][1] = a;
        queries[k][2] = b;
        queries[k][3] = c;
    }
    int64_t check = 0;
    for (int r = 0; r < 10; r++) {
        for (int k = 0; k < Q; k++) {
            check = (check * 131 + nth_ugly_number(queries[k][0], queries[k][1], queries[k][2], queries[k][3])) % 1000000007;
        }
    }
    printf("10 rounds of 50000 queries: checksum %lld\n", (long long)check);
    free(queries);
    return 0;
}
