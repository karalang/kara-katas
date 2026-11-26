// LeetCode #1774: Closest Dessert Cost -- the bench in C, mirroring
// closest_cost.kara: a depth-first search over the toppings for each base.
#include <stdio.h>
#include <stdlib.h>

static int better(int cost, int best, int target) {
    int d = abs(cost - target), e = abs(best - target);
    return d < e || (d == e && cost < best);
}

static void add_toppings(const int *toppings, int m, int i, int cost, int target, int *best) {
    if (better(cost, *best, target)) *best = cost;
    if (i == m || cost >= target) return;
    for (int times = 0; times < 3; times++)
        add_toppings(toppings, m, i + 1, cost + times * toppings[i], target, best);
}

static int closest_cost(const int *base_costs, int n, const int *topping_costs, int m, int target) {
    int best = base_costs[0];
    for (int b = 0; b < n; b++) add_toppings(topping_costs, m, 0, base_costs[b], target, &best);
    return best;
}

static long long seed = 1774;
static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int bases[100][10], toppings[100][8];
    for (int r = 0; r < 100; r++) {
        for (int i = 0; i < 10; i++) bases[r][i] = (int)(1 + next_random() % 5000);
        for (int i = 0; i < 8; i++) toppings[r][i] = (int)(1 + next_random() % 1000);
    }
    long long check = 0;
    for (long long call = 0; call < 1000; call++) {
        int target = (int)(1 + (check + call * 7919) % 10000);
        int cost = closest_cost(bases[(check + call) % 100], 10, toppings[(check / 100 + call * 31) % 100], 8, target);
        check = (check * 31 + cost) % 1000000007;
    }
    printf("1000 calls over 100 menus: checksum %lld\n", check);
    return 0;
}
