// LeetCode #1375 bench -- C: the ★ arm: after step i the string is
// aligned exactly when the largest bit flipped so far is i.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int num_times_all_blue(const int *flips, int64_t n) {
    int largest = 0;
    int aligned = 0;
    for (int64_t i = 0; i < n; i++) {
        if (flips[i] > largest) largest = flips[i];
        if (largest == i + 1) aligned++;
    }
    return aligned;
}

static int64_t seed = 1375;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    // 20 orders of 5 * 10^4 bits, the constraints' most, 1 to n shuffled
    // within runs of 2 to 8, built once; then 1000 rounds, each trading
    // two neighbouring flips of one order, both drawn from the checksum
    // so far, and counting that order's aligned steps
    enum { N = 50000, ORDERS = 20 };
    int *orders[ORDERS];
    for (int o = 0; o < ORDERS; o++) {
        int *flips = malloc(sizeof(int) * N);
        for (int v = 0; v < N; v++) flips[v] = v + 1;
        int64_t start = 0;
        while (start < N) {
            int64_t end = start + 2 + next_random() % 7;
            if (end > N) end = N;
            for (int64_t i = end - 1; i > start; i--) {
                int64_t j = start + next_random() % (i - start + 1);
                int t = flips[i];
                flips[i] = flips[j];
                flips[j] = t;
            }
            start = end;
        }
        orders[o] = flips;
    }
    int64_t check = 0;
    for (int64_t r = 0; r < 1000; r++) {
        int *flips = orders[check % ORDERS];
        int64_t k = (check / ORDERS) % (N - 1);
        int t = flips[k];
        flips[k] = flips[k + 1];
        flips[k + 1] = t;
        int64_t got = num_times_all_blue(flips, N);
        check = (check * 31 + got + r) % 1000000007;
    }
    printf("1000 rounds over 20 orders of 50000 bits: checksum %lld\n", (long long)check);
    return 0;
}
