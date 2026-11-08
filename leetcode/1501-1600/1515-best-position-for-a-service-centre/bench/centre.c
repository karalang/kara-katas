// LeetCode #1515 bench: the ★ arm's ternary search twice, as centre.kara.
// __builtin_sqrt and a hand floor keep the link free of -lm.
#include <stdint.h>
#include <stdio.h>

static double cost(const int64_t *xs, const int64_t *ys, int n, double x, double y) {
    double total = 0.0;
    for (int i = 0; i < n; i++) {
        double dx = (double)xs[i] - x;
        double dy = (double)ys[i] - y;
        total += __builtin_sqrt(dx * dx + dy * dy);
    }
    return total;
}

static double best_on(const int64_t *xs, const int64_t *ys, int n, double x) {
    double lo = 0.0, hi = 100.0;
    for (int r = 0; r < 60; r++) {
        double m1 = lo + (hi - lo) / 3.0;
        double m2 = hi - (hi - lo) / 3.0;
        if (cost(xs, ys, n, x, m1) < cost(xs, ys, n, x, m2)) hi = m2;
        else lo = m1;
    }
    return cost(xs, ys, n, x, (lo + hi) / 2.0);
}

static double get_min_dist_sum(const int64_t *xs, const int64_t *ys, int n) {
    double lo = 0.0, hi = 100.0;
    for (int r = 0; r < 60; r++) {
        double m1 = lo + (hi - lo) / 3.0;
        double m2 = hi - (hi - lo) / 3.0;
        if (best_on(xs, ys, n, m1) < best_on(xs, ys, n, m2)) hi = m2;
        else lo = m1;
    }
    return best_on(xs, ys, n, (lo + hi) / 2.0);
}

static int64_t seed = 1515;
static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t check = 0;
    int64_t xs[50], ys[50];
    for (int s = 0; s < 100; s++) {
        for (int i = 0; i < 50; i++) {
            xs[i] = next_random() % 101;
            ys[i] = next_random() % 101;
        }
        double answer = get_min_dist_sum(xs, ys, 50);
        int64_t hundredths = (int64_t)(answer * 100.0 + 0.5); // answer >= 0, so truncation is floor
        check = (check * 31 + hundredths + 1) % 1000000007;
    }
    printf("100 sets of 50 customers on 0..100: checksum %lld\n", (long long)check);
    return 0;
}
