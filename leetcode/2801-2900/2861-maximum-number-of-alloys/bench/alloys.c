// LeetCode #2861: Maximum Number of Alloys -- the bench: the ★ arm over
// 100 cases of 100 metals and 100 machines, LeetCode's most, amounts
// drawn over LeetCode's full ranges, all drawn first, then each
// answered 20 times.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 100

typedef struct {
    int64_t budget;
    int64_t composition[N][N];
    int64_t stock[N], cost[N];
} Case;

static int64_t price(const int64_t *machine, const int64_t *stock, const int64_t *cost, int64_t n, int64_t x) {
    int64_t sum = 0;
    for (int64_t j = 0; j < n; j++) {
        int64_t short_by = machine[j] * x - stock[j];
        sum += (short_by > 0 ? short_by : 0) * cost[j];
    }
    return sum;
}

static int64_t max_number_of_alloys(int64_t n, int64_t k, int64_t budget, int64_t composition[][N], const int64_t *stock, const int64_t *cost) {
    int64_t best = 0;
    for (int64_t i = 0; i < k; i++) {
        int64_t lo = 0, hi = 200000000;
        while (lo < hi) {
            int64_t mid = (lo + hi + 1) / 2;
            if (price(composition[i], stock, cost, n, mid) <= budget)
                lo = mid;
            else
                hi = mid - 1;
        }
        if (lo > best) best = lo;
    }
    return best;
}

static int64_t seed = 2861;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}
static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    const int64_t count = 100, rounds = 20;
    Case *cases = malloc(sizeof(Case) * count);
    for (int64_t c = 0; c < count; c++) {
        for (int64_t i = 0; i < N; i++)
            for (int64_t j = 0; j < N; j++) cases[c].composition[i][j] = 1 + wide() % 100;
        for (int64_t j = 0; j < N; j++) cases[c].stock[j] = wide() % 100000001;
        for (int64_t j = 0; j < N; j++) cases[c].cost[j] = 1 + wide() % 100;
        cases[c].budget = wide() % 100000001;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t c = 0; c < count; c++) {
            int64_t alloys = max_number_of_alloys(N, N, cases[c].budget, cases[c].composition, cases[c].stock, cases[c].cost);
            total += alloys;
            check = (check * 31 + alloys + r) % 1000000007;
        }
    }
    printf("%lld cases of %d by %d, %lld rounds: %lld alloys, checksum %lld\n", (long long)count, N, N, (long long)rounds, (long long)total, (long long)check);
    free(cases);
    return 0;
}
