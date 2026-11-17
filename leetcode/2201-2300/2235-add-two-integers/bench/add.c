// LeetCode #2235: Add Two Integers -- the benchmark's C mirror of
// add.kara: 10^7 pairs drawn and added, folded into a checksum.
#include <stdint.h>
#include <stdio.h>

static int64_t sum(int64_t num1, int64_t num2) {
    return num1 + num2;
}

static int64_t seed = 2235;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0;
    for (int64_t i = 0; i < 10000000; i++) {
        int64_t num1 = next_random() % 201 - 100;
        int64_t num2 = next_random() % 201 - 100;
        check = (check * 31 + sum(num1, num2) + 200) % 1000000007;
    }
    printf("10^7 pairs: checksum %lld\n", (long long)check);
    return 0;
}
