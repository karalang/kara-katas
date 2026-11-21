// LeetCode #2488: Count Subarrays With Median K -- C mirror of the ★ arm's
// benchmark (median.kara): the same 20 orders and passes, the balances of
// the starts counted in an open-addressing hash table.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CAP (1 << 15)

static int64_t keys[CAP];
static int64_t counts[CAP];
static char used[CAP];

static size_t slot(int64_t key) {
    uint64_t h = (uint64_t)key * 0x9E3779B97F4A7C15ULL;
    size_t i = (size_t)(h >> 49);
    while (used[i] && keys[i] != key) {
        i = (i + 1) & (CAP - 1);
    }
    return i;
}

static void add(int64_t key) {
    size_t s = slot(key);
    if (!used[s]) {
        used[s] = 1;
        keys[s] = key;
        counts[s] = 0;
    }
    counts[s] += 1;
}

static int64_t get(int64_t key) {
    size_t s = slot(key);
    return used[s] ? counts[s] : 0;
}

static int64_t count_subarrays(const int64_t *nums, int64_t n, int64_t k) {
    int64_t at = 0;
    while (nums[at] != k) at++;
    memset(used, 0, sizeof used);
    add(0);
    int64_t balance = 0;
    for (int64_t i = at - 1; i >= 0; i--) {
        balance += nums[i] > k ? 1 : -1;
        add(balance);
    }
    int64_t count = 0;
    balance = 0;
    for (int64_t j = at; j < n; j++) {
        if (j > at) balance += nums[j] > k ? 1 : -1;
        count += get(-balance) + get(1 - balance);
    }
    return count;
}

static int64_t seed = 2488;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 10000, passes = 400;
    static int64_t orders[20][10000];
    for (int o = 0; o < 20; o++) {
        for (int64_t i = 0; i < n; i++) orders[o][i] = i + 1;
        for (int64_t i = n - 1; i >= 1; i--) {
            int64_t j = next_random() % (i + 1);
            int64_t t = orders[o][i];
            orders[o][i] = orders[o][j];
            orders[o][j] = t;
        }
    }
    int64_t check = 0;
    for (int64_t p = 0; p < passes; p++) {
        for (int64_t o = 0; o < 20; o++) {
            int64_t a = check % n, b = (check / n + p) % n;
            int64_t t = orders[o][a];
            orders[o][a] = orders[o][b];
            orders[o][b] = t;
            int64_t k = (check + o) % n + 1;
            check = (check * 31 + count_subarrays(orders[o], n, k) + p) % 1000000007;
        }
    }
    printf("%lld passes over 20 orders of 10^4: checksum %lld\n", (long long)passes, (long long)check);
    return 0;
}
