// Benchmark: LeetCode #964 Least Operators to Express Number -- the ★
// arm, digit DP, on every x from 2 to 100 and 2000 targets spread below
// LeetCode's largest, 2 * 10^8, each round's targets one higher than the
// last's. Mirrors least_ops_express_target.kara, .rs, .py and go-seq/.
#include <stdint.h>
#include <stdio.h>

static int64_t min64(int64_t a, int64_t b) { return a < b ? a : b; }

static int64_t least_ops_express_target(int64_t x, int64_t target) {
    int64_t t = target, pos = 0, neg = 0, k = 0;
    while (t > 0) {
        int64_t cur = t % x;
        t = t / x;
        if (k > 0) {
            int64_t p = min64(cur * k + pos, (cur + 1) * k + neg);
            int64_t n = min64((x - cur) * k + pos, (x - cur - 1) * k + neg);
            pos = p;
            neg = n;
        } else {
            pos = cur * 2;
            neg = (x - cur) * 2;
        }
        k++;
    }
    return min64(pos, k + neg) - 1;
}

int main(void) {
    int rounds = 80;
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int64_t x = 2; x < 101; x++) {
            for (int64_t j = 0; j < 2000; j++) {
                int64_t n = least_ops_express_target(x, 200000000 - 99991 * j - r);
                total += n;
                check = (check * 31 + n) % 1000000007;
            }
        }
    }
    printf("%d rounds over x from 2 to 100 and 2000 targets: %lld operators, checksum %lld\n", rounds,
           (long long)total, (long long)check);
    return 0;
}
