// LeetCode #1599: Maximum Profit of Operating a Centennial Wheel
// -- the bench in C, mirroring wheel.kara: the wheel run rotation by
// rotation in int64_t, on 300 days of 100000 arrivals, all drawn first.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int32_t min_operations_max_profit(const int32_t *customers, int64_t n, int32_t boarding_cost, int32_t running_cost) {
    int64_t waiting = 0, profit = 0, best = 0, rotations = 0;
    int32_t answer = -1;
    while (rotations < n || waiting > 0) {
        if (rotations < n) waiting += customers[rotations];
        int64_t board = waiting < 4 ? waiting : 4;
        waiting -= board;
        profit += board * boarding_cost - running_cost;
        rotations++;
        if (profit > best) {
            best = profit;
            answer = (int32_t)rotations;
        }
    }
    return answer;
}

int main(void) {
    enum { D = 300, N = 100000 };
    int64_t seed = 1599;
    int32_t **customers = malloc(sizeof(int32_t *) * D);
    int32_t boarding[D], running[D];
    for (int d = 0; d < D; d++) {
        customers[d] = malloc(sizeof(int32_t) * N);
        for (int i = 0; i < N; i++) {
            seed = (seed * 1103515245 + 12345) % 2147483648LL;
            customers[d][i] = (int32_t)(seed / 65536 % 9);
        }
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        boarding[d] = (int32_t)(seed / 65536 % 100 + 1);
        seed = (seed * 1103515245 + 12345) % 2147483648LL;
        running[d] = (int32_t)(seed / 65536 % 100 + 1);
    }
    int64_t check = 0;
    for (int d = 0; d < D; d++) {
        int32_t answer = min_operations_max_profit(customers[d], N, boarding[d], running[d]);
        check = (check * 31 + answer + 1) % 1000000007;
    }
    printf("300 days of 100000 arrivals: checksum %lld\n", (long long)check);
    for (int d = 0; d < D; d++) free(customers[d]);
    free(customers);
    return 0;
}
