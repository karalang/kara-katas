// LeetCode #2457: Minimum Addition to Make Integer Beautiful -- bench, C
// mirror of beautiful.kara: while the digit sum is too large, n + x is
// rounded up to the next multiple of a power of ten one place higher.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t digit_sum(int64_t x) {
    int64_t sum = 0;
    while (x > 0) {
        sum += x % 10;
        x /= 10;
    }
    return sum;
}

static int64_t make_integer_beautiful(int64_t n, int64_t target) {
    int64_t m = n, p = 1;
    while (digit_sum(m) > target) {
        p *= 10;
        m = (m + p - 1) / p * p;
    }
    return m - n;
}

static int64_t seed = 2457;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t *ns = malloc(sizeof(int64_t) * 100000);
    int64_t *ts = malloc(sizeof(int64_t) * 100000);
    for (int i = 0; i < 100000; i++) {
        int64_t a = next_random();
        int64_t b = next_random();
        ns[i] = 1 + (a * 1073741824 + b * 32768 + next_random()) % 1000000000000LL;
        ts[i] = next_random() % 150;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 36; p++) {
        for (int i = 0; i < 100000; i++) {
            check = (check * 31 + make_integer_beautiful(ns[i], 1 + (ts[i] + p) % 150) + p) % 1000000007;
        }
    }
    printf("36 passes over 10^5 pairs: checksum %lld\n", (long long)check);
    free(ns);
    free(ts);
    return 0;
}
