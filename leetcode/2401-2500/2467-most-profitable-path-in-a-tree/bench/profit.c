// LeetCode #2467: Most Profitable Path in a Tree -- the bench, the ★ arm in
// C: the adjacency lists packed by counting sort into one array, then
// breadth-first parents and depths from node 0, Bob's seconds up his
// parent chain, and each node's income its parent's plus its gate.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 10000

static int64_t start[N + 1], packed[2 * N], parent_[N], depth_[N], order_[N], bob_time[N], income_[N];

static int64_t most_profitable_path(const int64_t (*edges)[2], int64_t m, int64_t bob, const int64_t *amount, int64_t n) {
    for (int64_t i = 0; i <= n; i++) start[i] = 0;
    for (int64_t i = 0; i < m; i++) {
        start[edges[i][0] + 1]++;
        start[edges[i][1] + 1]++;
    }
    for (int64_t i = 0; i < n; i++) start[i + 1] += start[i];
    int64_t fill[N];
    for (int64_t i = 0; i < n; i++) fill[i] = start[i];
    for (int64_t i = 0; i < m; i++) {
        packed[fill[edges[i][0]]++] = edges[i][1];
        packed[fill[edges[i][1]]++] = edges[i][0];
    }
    for (int64_t i = 0; i < n; i++) {
        parent_[i] = -1;
        depth_[i] = 0;
    }
    int64_t len = 1;
    order_[0] = 0;
    parent_[0] = 0;
    for (int64_t next = 0; next < len; next++) {
        int64_t node = order_[next];
        for (int64_t k = start[node]; k < start[node + 1]; k++) {
            int64_t child = packed[k];
            if (parent_[child] < 0) {
                parent_[child] = node;
                depth_[child] = depth_[node] + 1;
                order_[len++] = child;
            }
        }
    }
    for (int64_t i = 0; i < n; i++) bob_time[i] = n;
    int64_t node = bob, t = 0;
    while (node != 0) {
        bob_time[node] = t;
        node = parent_[node];
        t++;
    }
    bob_time[0] = t;
    int64_t best = INT64_MIN;
    for (int64_t i = 0; i < n; i++) {
        int64_t v = order_[i];
        int64_t gate = depth_[v] < bob_time[v] ? amount[v] : depth_[v] == bob_time[v] ? amount[v] / 2 : 0;
        income_[v] = v == 0 ? gate : income_[parent_[v]] + gate;
        if (v != 0 && start[v + 1] - start[v] == 1 && income_[v] > best) best = income_[v];
    }
    return best;
}

static int64_t seed = 2467;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t trees[10][N - 1][2];
static int64_t amounts[10][N];

int main(void) {
    // 10 random trees of 10^4 nodes built once, each node joined to an
    // earlier one, with even amounts from -10^4 to 10^4; then 140
    // passes, each moving every tree's Bob and setting one amount from the
    // checksum so far, then answering it and folding the answer plus the
    // pass into the checksum
    int64_t n = N;
    for (int a = 0; a < 10; a++) {
        for (int64_t node = 1; node < n; node++) {
            int64_t r = next_random();
            int64_t s = next_random();
            trees[a][node - 1][0] = node;
            trees[a][node - 1][1] = (r * 32768 + s) % node;
        }
        for (int64_t i = 0; i < n; i++) amounts[a][i] = 2 * (next_random() % 10001) - 10000;
    }
    int64_t check = 0;
    for (int64_t p = 0; p < 140; p++) {
        for (int64_t a = 0; a < 10; a++) {
            int64_t bob = 1 + check % (n - 1);
            amounts[a][(check + a) % n] = 2 * (check % 10001) - 10000;
            int64_t got = most_profitable_path((const int64_t (*)[2])trees[a], n - 1, bob, amounts[a], n);
            check = ((check * 31 + got + p) % 1000000007 + 1000000007) % 1000000007;
        }
    }
    printf("140 passes over 10 trees of 10^4: checksum %lld\n", (long long)check);
    return 0;
}
