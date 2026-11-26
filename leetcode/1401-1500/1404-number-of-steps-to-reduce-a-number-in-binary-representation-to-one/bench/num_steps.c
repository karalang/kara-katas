// LeetCode #1404 bench, C: the same walk with a carry, workload and
// checksum as num_steps.kara.
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define POOL 100000
#define DIGITS 500

static int32_t num_steps(const char *s, int n) {
    int32_t steps = 0, carry = 0;
    for (int i = n - 1; i >= 1; i--) {
        int32_t bit = (s[i] == '1' ? 1 : 0) + carry;
        if (bit == 1) {
            steps += 2;
            carry = 1;
        } else {
            steps += 1;
        }
    }
    return steps + carry;
}

int main(void) {
    static char pool[POOL];
    int64_t seed = 1404;
    for (int i = 0; i < POOL; i++) {
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        pool[i] = seed / 65536 % 2 == 0 ? '0' : '1';
    }
    int64_t check = 0;
    char s[DIGITS];
    for (int64_t r = 0; r < 200000; r++) {
        int64_t at = (check + r * 7919) % 99501;
        s[0] = '1';
        memcpy(s + 1, pool + at, DIGITS - 1);
        check = (check * 131 + num_steps(s, DIGITS)) % 1000000007;
    }
    printf("200000 numbers of 500 digits: checksum %lld\n", (long long)check);
    return 0;
}
