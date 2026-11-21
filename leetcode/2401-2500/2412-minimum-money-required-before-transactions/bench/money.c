// LeetCode #2412: Minimum Money Required Before Transactions -- the bench,
// the ★ arm in C: the total loss, and the largest of the losing
// transactions' cashbacks and the gaining ones' costs.

#include <stdint.h>
#include <stdio.h>

#define N 100000

static int64_t seed = 2412;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t minimum_money(const int64_t (*t)[2], int64_t n) {
    int64_t loss = 0, extra = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t cost = t[i][0], cashback = t[i][1];
        if (cost > cashback) {
            loss += cost - cashback;
            if (cashback > extra) extra = cashback;
        } else if (cost > extra) {
            extra = cost;
        }
    }
    return loss + extra;
}

int main(void) {
    static int64_t lists[10][N][2];
    int64_t top = 1;
    for (int i = 0; i < 10; i++) {
        top *= 7;
        for (int j = 0; j < N; j++) {
            lists[i][j][0] = (next_random() * 32768 + next_random()) % (top + 1);
            lists[i][j][1] = (next_random() * 32768 + next_random()) % (top + 1);
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 100; p++)
        for (int i = 0; i < 10; i++) check = (check * 31 + minimum_money((const int64_t (*)[2])lists[i], N) + p) % 1000000007;
    printf("100 passes over 10 lists of 10^5 transactions: checksum %lld\n", (long long)check);
    return 0;
}
