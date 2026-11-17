// LeetCode #2240: Number of Ways to Buy Pens and Pencils -- the
// benchmark's C mirror of ways.kara: for each number of pens, the
// pencils the rest buys plus none, summed.
#include <stdint.h>
#include <stdio.h>

static int64_t ways_to_buy_pens_pencils(int64_t total, int64_t cost1, int64_t cost2) {
    int64_t ways = 0;
    for (int64_t pens = 0; pens * cost1 <= total; pens++) ways += (total - pens * cost1) / cost2 + 1;
    return ways;
}

static int64_t seed = 2240;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide_random(void) {
    int64_t high = next_random();
    return high * 32768 + next_random();
}

int main(void) {
    int64_t check = 0;
    for (int c = 0; c < 300; c++) {
        // the money at 10^6, a pen from 1 to 10, a pencil up to 10^6
        int64_t cost1 = next_random() % 10 + 1;
        int64_t cost2 = wide_random() % 1000000 + 1;
        check = (check * 31 + ways_to_buy_pens_pencils(1000000, cost1, cost2)) % 1000000007;
    }
    printf("300 cases of 10^6 money: checksum %lld\n", (long long)check);
    return 0;
}
