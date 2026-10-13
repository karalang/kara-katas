// Benchmark for #465: mirror of min_transfers.kara (the ★ arm:
// backtracking over the unsettled balances) on the same workload.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t fewest_from(int64_t *debts, int64_t len, int64_t start) {
    int64_t first = start;
    while (first < len && debts[first] == 0) {
        first += 1;
    }
    if (first == len) {
        return 0;
    }
    int64_t best = -1;
    for (int64_t j = first + 1; j < len; j++) {
        if (debts[j] * debts[first] < 0) {
            debts[j] += debts[first];
            int64_t count = 1 + fewest_from(debts, len, first + 1);
            debts[j] -= debts[first];
            if (best < 0 || count < best) {
                best = count;
            }
        }
    }
    return best;
}

static int64_t min_transfers(const int64_t (*transactions)[3], int64_t n) {
    int64_t people = 0;
    for (int64_t t = 0; t < n; t++) {
        if (transactions[t][0] + 1 > people) people = transactions[t][0] + 1;
        if (transactions[t][1] + 1 > people) people = transactions[t][1] + 1;
    }
    int64_t *balance = calloc(people, sizeof(int64_t));
    for (int64_t t = 0; t < n; t++) {
        balance[transactions[t][0]] -= transactions[t][2];
        balance[transactions[t][1]] += transactions[t][2];
    }
    int64_t *debts = malloc(people * sizeof(int64_t));
    int64_t len = 0;
    for (int64_t p = 0; p < people; p++) {
        if (balance[p] != 0) {
            debts[len++] = balance[p];
        }
    }
    int64_t result = fewest_from(debts, len, 0);
    free(balance);
    free(debts);
    return result;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    const int64_t ledgers = 20000;
    int64_t seed = 465;
    int64_t total = 0;
    int64_t checksum = 0;
    int64_t transactions[8][3];
    for (int64_t l = 0; l < ledgers; l++) {
        for (int t = 0; t < 8; t++) {
            int64_t from = next_random(&seed) % 12;
            int64_t to = (from + 1 + next_random(&seed) % 11) % 12;
            int64_t amount = 1 + next_random(&seed) % 3;
            transactions[t][0] = from;
            transactions[t][1] = to;
            transactions[t][2] = amount;
        }
        int64_t fewest = min_transfers((const int64_t (*)[3])transactions, 8);
        total += fewest;
        checksum = (checksum * 31 + fewest) % 1000000007;
    }
    printf("%lld ledgers of 8 transactions: %lld transfers in all, checksum %lld\n", (long long)ledgers,
           (long long)total, (long long)checksum);
    return 0;
}
