// LeetCode #1824: Minimum Sideway Jumps -- the bench in C: the ★ arm over
// 50 calls on roads of 250000 to 499999 steps cut from one road of
// 5 * 10^5 steps with an obstacle at half its points, built once, each
// road's length drawn from the checksum so far and its last point cleared.
// Each call is handed its own copy of the road, as `to_vec` makes one.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t min3(const int64_t *j) {
    int64_t m = j[0];
    if (j[1] < m) m = j[1];
    if (j[2] < m) m = j[2];
    return m;
}

static int64_t min_side_jumps(const int64_t *obstacles, size_t n) {
    int64_t never = (int64_t)n + 1;
    int64_t jumps[3] = {1, 0, 1};
    for (size_t i = 1; i < n; i++) {
        if (obstacles[i] > 0) jumps[obstacles[i] - 1] = never;
        int64_t best = min3(jumps) + 1;
        for (int64_t lane = 0; lane < 3; lane++)
            if (obstacles[i] != lane + 1 && best < jumps[lane]) jumps[lane] = best;
    }
    return min3(jumps);
}

static int64_t seed = 1824;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    static int64_t base[500001];
    for (int i = 1; i < 500000; i++)
        if (next_random() % 2 == 0) base[i] = 1 + next_random() % 3;
    int64_t check = 0;
    for (int64_t call = 0; call < 50; call++) {
        size_t n = (size_t)(250000 + (check + call) % 250000);
        int64_t *road = malloc((n + 1) * sizeof *road);
        memcpy(road, base, (n + 1) * sizeof *road);
        road[n] = 0;
        check = (check * 31 + min_side_jumps(road, n + 1)) % 1000000007;
        free(road);
    }
    printf("50 calls: checksum %lld\n", (long long)check);
    return 0;
}
