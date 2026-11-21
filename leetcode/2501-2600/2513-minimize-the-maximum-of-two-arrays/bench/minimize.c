// LeetCode #2513: Minimize the Maximum of Two Arrays -- C mirror of the
// benchmark (minimize.kara): the same cases, passes and checksum.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t gcd(int64_t a, int64_t b) {
    while (b != 0) {
        int64_t r = a % b;
        a = b;
        b = r;
    }
    return a;
}

static int64_t minimize_set(int64_t d1, int64_t d2, int64_t c1, int64_t c2) {
    int64_t lcm = d1 / gcd(d1, d2) * d2;
    int64_t lo = 1, hi = 2 * (c1 + c2);
    while (lo < hi) {
        int64_t mid = lo + (hi - lo) / 2;
        if (mid - mid / d1 >= c1 && mid - mid / d2 >= c2 && mid - mid / lcm >= c1 + c2) hi = mid;
        else lo = mid + 1;
    }
    return lo;
}

static int64_t seed = 2513;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t below(int64_t top) {
    int64_t hi = next_random();
    return (hi * 32768 + next_random()) % top;
}

int main(void) {
    int64_t (*cases)[4] = malloc(100000 * sizeof *cases);
    for (int i = 0; i < 100000; i++) {
        cases[i][0] = below(99999) + 2;
        cases[i][1] = below(99999) + 2;
        cases[i][2] = below(999998999) + 1;
        cases[i][3] = below(999999000 - cases[i][2]) + 1;
    }
    const int64_t passes = 10;
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++)
        for (int i = 0; i < 100000; i++)
            check = (check * 31 + minimize_set(cases[i][0], cases[i][1], cases[i][2] + check % 1000, cases[i][3]) + p) % 1000000007;
    printf("%lld passes over 10^5 cases: checksum %lld\n", (long long)passes, (long long)check);
    free(cases);
    return 0;
}
