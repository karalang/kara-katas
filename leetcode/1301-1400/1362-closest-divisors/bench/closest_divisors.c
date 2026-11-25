// LeetCode #1362 bench -- C: d counts down from the square root of num + 2,
// and the first d that divides num + 1 or num + 2 gives the answer.
#include <math.h>
#include <stdint.h>
#include <stdio.h>

static int64_t isqrt(int64_t x) {
    int64_t r = (int64_t)sqrt((double)x);
    while (r * r > x) r--;
    while ((r + 1) * (r + 1) <= x) r++;
    return r;
}

static void closest_divisors(int32_t num, int32_t out[2]) {
    int64_t one = (int64_t)num + 1, two = (int64_t)num + 2;
    for (int64_t d = isqrt(two); d > 0; d--) {
        if (one % d == 0) {
            out[0] = (int32_t)d;
            out[1] = (int32_t)(one / d);
            return;
        }
        if (two % d == 0) {
            out[0] = (int32_t)d;
            out[1] = (int32_t)(two / d);
            return;
        }
    }
    out[0] = 1;
    out[1] = num + 1;
}

int main(void) {
    // 10^4 questions, each num up to 10^9 drawn from the checksum so far,
    // both parts of every answer folded into it
    int64_t check = 0;
    for (int64_t r = 0; r < 10000; r++) {
        int32_t num = (int32_t)(1 + (check * 7919 + r) % 1000000000);
        int32_t pair[2];
        closest_divisors(num, pair);
        check = (check * 31 + (int64_t)pair[0] * 7 + pair[1] + r) % 1000000007;
    }
    printf("10000 questions: checksum %lld\n", (long long)check);
    return 0;
}
