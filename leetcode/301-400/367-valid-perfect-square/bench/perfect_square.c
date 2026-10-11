// Benchmark for #367 -- mirror of perfect_square.kara.
#include <stdint.h>
#include <stdio.h>

static int is_perfect_square(int64_t num) {
    int64_t lo = 1, hi = num;
    while (lo <= hi) {
        int64_t mid = lo + (hi - lo) / 2;
        int64_t sq = mid * mid;
        if (sq == num) return 1;
        if (sq < num) lo = mid + 1;
        else hi = mid - 1;
    }
    return 0;
}

int main(void) {
    int64_t seed = 367, yes = 0, checksum = 0;
    for (int64_t i = 0; i < 3000000; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t high = seed / 65536;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        int64_t wide = high * 32768 + seed / 65536;
        int64_t num;
        if (i % 2 == 0) {
            int64_t r = 1 + wide % 46340;
            num = r * r;
        } else {
            num = 1 + wide + (i / 2 % 2) * 1073741823;
        }
        if (is_perfect_square(num)) {
            yes++;
            checksum = (checksum * 31 + i) % 1000000007;
        }
    }
    printf("%lld squares, checksum %lld\n", (long long)yes, (long long)checksum);
    return 0;
}
