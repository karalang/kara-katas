// LeetCode #2813: Maximum Elegance of a K-Length Subsequence -- the bench
// in C: the ★ arm over 10 cases of 10^5 items, profits up to 10^9 and
// categories up to 30000, k from 1 to 10^5, all drawn first, then each
// answered 5 times. The items are copied and sorted by `qsort`, the
// categories taken marked in an array indexed by category, and the
// repeats kept on an array stack.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define N 100000
#define COUNT 10
#define KINDS 30000

typedef struct {
    int64_t profit, category;
} Item;

static int64_t seed = 2813;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static int dearest_first(const void *x, const void *y) {
    int64_t a = ((const Item *)x)->profit, b = ((const Item *)y)->profit;
    return (a < b) - (a > b);
}

static Item cases[COUNT][N];
static int64_t ks[COUNT];
static Item order[N];
static char seen[KINDS + 1];
static int64_t repeats[N];

static int64_t find_maximum_elegance(const Item *items, int64_t n, int64_t k) {
    memcpy(order, items, sizeof(Item) * n);
    qsort(order, n, sizeof(Item), dearest_first);
    memset(seen, 0, sizeof seen);
    int64_t distinct = 0, top = 0, total = 0;
    for (int64_t i = 0; i < k; i++) {
        total += order[i].profit;
        if (seen[order[i].category])
            repeats[top++] = order[i].profit;
        else {
            seen[order[i].category] = 1;
            distinct++;
        }
    }
    int64_t best = total + distinct * distinct;
    for (int64_t i = k; i < n; i++) {
        if (top == 0) break;
        if (!seen[order[i].category]) {
            seen[order[i].category] = 1;
            distinct++;
            total += order[i].profit - repeats[--top];
            int64_t score = total + distinct * distinct;
            if (score > best) best = score;
        }
    }
    return best;
}

int main(void) {
    int rounds = 5;
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < N; i++) {
            cases[c][i].profit = wide() % 1000000000 + 1;
            cases[c][i].category = wide() % KINDS + 1;
        }
        ks[c] = wide() % N + 1;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++)
        for (int c = 0; c < COUNT; c++) {
            int64_t a = find_maximum_elegance(cases[c], N, ks[c]);
            total += a;
            check = (check * 31 + a % 1000000007 + r) % 1000000007;
        }
    printf("%d cases of %d, %d rounds: elegance sums to %lld, checksum %lld\n", COUNT, N, rounds, (long long)total, (long long)check);
    return 0;
}
