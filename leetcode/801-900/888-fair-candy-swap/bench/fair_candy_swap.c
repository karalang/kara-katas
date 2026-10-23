// LeetCode #888 bench: a set of Bob's boxes, on 2000 cases of 5,000 to
// 10^4 boxes each, up to 10^5 candies a box. The same algorithm as
// fair_candy_swap.kara; C has no set, so Bob's boxes go in an
// open-addressing hash table with linear probing.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define SLOTS 32768

static int64_t table[SLOTS];

static void fair_candy_swap(const int64_t *alice, int64_t n, const int64_t *bob, int64_t m, int64_t *swap) {
    memset(table, 0, sizeof table);
    int64_t alice_total = 0, bob_total = 0;
    for (int64_t i = 0; i < n; i++) alice_total += alice[i];
    for (int64_t j = 0; j < m; j++) {
        bob_total += bob[j];
        uint64_t h = ((uint64_t)bob[j] * 0x9E3779B97F4A7C15ull) >> 49;
        while (table[h] != 0 && table[h] != bob[j]) h = (h + 1) & (SLOTS - 1);
        table[h] = bob[j];
    }
    int64_t d = (bob_total - alice_total) / 2;
    int64_t best = -1;
    for (int64_t i = 0; i < n; i++) {
        int64_t want = alice[i] + d;
        if (want < 1) continue;
        uint64_t h = ((uint64_t)want * 0x9E3779B97F4A7C15ull) >> 49;
        while (table[h] != 0 && table[h] != want) h = (h + 1) & (SLOTS - 1);
        if (table[h] == want && (best < 0 || alice[i] < best)) best = alice[i];
    }
    swap[0] = best;
    swap[1] = best + d;
}

static int64_t seed = 888;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t below(int64_t limit) {
    int64_t hi = next_random();
    return (hi * 32768 + next_random()) % limit;
}

static int64_t alice[10001], bob[10001];

static int64_t max64(int64_t a, int64_t b) { return a > b ? a : b; }
static int64_t min64(int64_t a, int64_t b) { return a < b ? a : b; }

// as in the Kāra bench: Alice's n boxes and Bob's m with a swap that
// evens the totals
static int64_t case_boxes(int64_t n, int64_t m, int64_t most) {
    for (;;) {
        int64_t alice_total = 0;
        for (int64_t k = 0; k < n; k++) {
            alice[k] = 1 + below(most);
            alice_total += alice[k];
        }
        for (int64_t k = 0; k < m; k++) bob[k] = 1 + below(most);
        int64_t i = below(n);
        int64_t j = below(m);
        int64_t y = 1 + below(most);
        bob[j] = y;
        int64_t bob_total = 0;
        for (int64_t k = 0; k < m; k++) bob_total += bob[k];
        int64_t short_by = alice_total + 2 * (y - alice[i]) - bob_total;
        for (int64_t k = 0; k < m; k++) {
            if (k != j && short_by != 0) {
                int64_t step = min64(max64(short_by, 1 - bob[k]), most - bob[k]);
                bob[k] += step;
                short_by -= step;
            }
        }
        for (int64_t k = 0; k < n; k++) {
            if (k != i && short_by != 0) {
                int64_t step = min64(max64(-short_by, 1 - alice[k]), most - alice[k]);
                alice[k] += step;
                short_by += step;
            }
        }
        if (short_by == 0 && y != alice[i]) return m;
    }
}

int main(void) {
    int64_t gives = 0, takes = 0, check = 0, swap[2];
    for (int c = 0; c < 2000; c++) {
        int64_t n = 5000 + below(5001);
        int64_t m = 5000 + below(5001);
        case_boxes(n, m, 100000);
        fair_candy_swap(alice, n, bob, m, swap);
        gives += swap[0];
        takes += swap[1];
        check = (check * 131 + swap[0] * 7 + swap[1]) % 1000000007;
    }
    printf("2000 cases of 5000 to 10000 boxes: Alice gives %lld candies, Bob %lld, checksum %lld\n",
           (long long)gives, (long long)takes, (long long)check);
    return 0;
}
