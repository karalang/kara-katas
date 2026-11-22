// LeetCode #2806: Account Balance After Rounded Purchase -- the bench in
// C: the ★ arm over 10^6 amounts from 0 to 100, all drawn first, then
// each answered 100 times into a running checksum.
#include <stdint.h>
#include <stdio.h>

#define COUNT 1000000

static int64_t seed = 2806;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t account_balance_after_purchase(int64_t purchase_amount) {
    return 100 - (purchase_amount + 5) / 10 * 10;
}

static int64_t amounts[COUNT];

int main(void) {
    int rounds = 100;
    for (int i = 0; i < COUNT; i++) amounts[i] = next_random() % 101;
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int i = 0; i < COUNT; i++) {
            int64_t b = account_balance_after_purchase(amounts[i]);
            total += b;
            check = (check * 31 + b + r) % 1000000007;
        }
    }
    printf("%d amounts, %d rounds: balances sum to %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
