// LeetCode #1518 bench: the ★ arm (whole lots a round), as bottles.kara.
#include <stdint.h>
#include <stdio.h>

static int64_t num_water_bottles(int64_t num_bottles, int64_t num_exchange) {
    int64_t drunk = 0, full = num_bottles, empty = 0;
    while (full > 0) {
        drunk += full;
        empty += full;
        full = empty / num_exchange;
        empty %= num_exchange;
    }
    return drunk;
}

int main(void) {
    int64_t check = 0;
    for (int64_t i = 0; i < 20000000; i++) {
        int64_t bottles = i * 7919 % 1000000000 + 1;
        int64_t exchange = i % 99 + 2;
        check = (check * 31 + num_water_bottles(bottles, exchange) + 1) % 1000000007;
    }
    printf("20000000 questions up to 10^9 bottles and 2 to 100 for 1: checksum %lld\n", (long long)check);
    return 0;
}
