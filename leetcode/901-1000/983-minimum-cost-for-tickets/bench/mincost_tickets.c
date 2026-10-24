// Benchmark: LeetCode #983 Minimum Cost For Tickets -- the ★ arm, a
// table over the calendar, on plans of up to LeetCode's 365 days.
// Mirrors mincost_tickets.kara, .rs, .py and go-seq/.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t min64(int64_t a, int64_t b) { return a < b ? a : b; }

static int64_t mincost_tickets(const int64_t *days, int n, const int64_t *costs) {
    int64_t last = days[n - 1];
    bool *travel = calloc((size_t)last + 1, sizeof(bool));
    for (int i = 0; i < n; i++) {
        travel[days[i]] = true;
    }
    int64_t *best = calloc((size_t)last + 1, sizeof(int64_t));
    for (int64_t d = 1; d <= last; d++) {
        if (!travel[d]) {
            best[d] = best[d - 1];
            continue;
        }
        int64_t week = d >= 7 ? best[d - 7] : 0;
        int64_t month = d >= 30 ? best[d - 30] : 0;
        best[d] = min64(min64(best[d - 1] + costs[0], week + costs[1]), month + costs[2]);
    }
    int64_t out = best[last];
    free(travel);
    free(best);
    return out;
}

static int64_t seed = 983;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int rounds = 300;
    static int64_t plans[1000][365];
    static int sizes[1000];
    static int64_t prices[1000][3];
    for (int p = 0; p < 1000; p++) {
        int64_t n = 1 + next_random() % 365;
        int64_t need = n;
        int k = 0;
        for (int64_t d = 1; d < 366; d++) {
            if (need > 0 && next_random() % (366 - d) < need) {
                plans[p][k++] = d;
                need--;
            }
        }
        sizes[p] = k;
        for (int c = 0; c < 3; c++) {
            prices[p][c] = 1 + next_random() % 1000;
        }
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < 1000; i++) {
            int j = (r + i) % 1000;
            int64_t c = mincost_tickets(plans[j], sizes[j], prices[j]);
            total += c;
            check = (check * 31 + c) % 1000000007;
        }
    }
    printf("%d rounds over 1000 plans of up to 365 days: cost %lld, checksum %lld\n", rounds, (long long)total,
           (long long)check);
    return 0;
}
