// LeetCode #878 bench: C mirror of nth_magical_number.kara (the ★ arm,
// binary search on the answer) on the same 1,000,000 cases.

#include <stdint.h>
#include <stdio.h>

static int64_t gcd(int64_t a, int64_t b) {
    return b == 0 ? a : gcd(b, a % b);
}

static int64_t nth_magical_number(int64_t n, int64_t a, int64_t b) {
    int64_t lcm = a / gcd(a, b) * b;
    int64_t lo = 1, hi = n * (a < b ? a : b);
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (mid / a + mid / b - mid / lcm >= n) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    return lo % 1000000007;
}

static int64_t seed = 878;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t up_to(int64_t limit) {
    int64_t x = next_random();
    int64_t y = next_random();
    return (x * 32768 + y) % limit + 1;
}

int main(void) {
    int64_t total = 0, check = 0;
    for (int k = 0; k < 1000000; k++) {
        int64_t n = up_to(1000000000);
        int64_t a = up_to(39999) + 1;
        int64_t b = up_to(39999) + 1;
        int64_t answer = nth_magical_number(n, a, b);
        total += answer;
        check = (check * 131 + answer) % 1000000007;
    }
    printf("1000000 cases: answers sum to %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
