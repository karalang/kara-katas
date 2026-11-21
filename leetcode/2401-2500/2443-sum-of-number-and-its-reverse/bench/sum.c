// LeetCode #2443: Sum of Number and Its Reverse -- the bench, the ★ arm:
// every `k` from 0 to `num` tried, its digits reversed by `% 10` and
// `/ 10`.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

static int64_t reversed(int64_t x) {
    int64_t r = 0, y = x;
    while (y > 0) {
        r = r * 10 + y % 10;
        y /= 10;
    }
    return r;
}

static bool sum_of_number_and_reverse(int64_t num) {
    for (int64_t k = 0; k <= num; k++)
        if (k + reversed(k) == num) return true;
    return false;
}

static int64_t seed = 2443;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0;
    for (int64_t i = 0; i < 400; i++) {
        int64_t a = next_random();
        int64_t num = 90000 + (a * 32768 + next_random()) % 10001;
        int64_t verdict = sum_of_number_and_reverse(num) ? 1 : 0;
        check = (check * 31 + num * 2 + verdict + i) % 1000000007;
    }
    printf("400 nums near 10^5: checksum %lld\n", (long long)check);
    return 0;
}
