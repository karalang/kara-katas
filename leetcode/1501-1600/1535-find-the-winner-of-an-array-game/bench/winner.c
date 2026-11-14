// LeetCode #1535: Find the Winner of an Array Game -- bench: the ★ arm
// over 100 random arrays of 100000 distinct values, each with its own k
// from 1 to 200000, built once and answered 20 times. C mirror of
// winner.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t get_winner(const int64_t *arr, int64_t n, int64_t k) {
    int64_t front = arr[0], streak = 0;
    for (int64_t i = 1; i < n; i++) {
        if (arr[i] > front) {
            front = arr[i];
            streak = 1;
        } else {
            streak += 1;
        }
        if (streak == k) {
            return front;
        }
    }
    return front;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

static int64_t draw(int64_t *seed, int64_t below) {
    int64_t hi = next_random(seed);
    return (hi * 32768 + next_random(seed)) % below;
}

int main(void) {
    int64_t seed = 1535;
    const int64_t n = 100000;
    int64_t *arrs[100];
    int64_t ks[100];
    for (int p = 0; p < 100; p++) {
        int64_t *arr = malloc(n * sizeof(int64_t));
        for (int64_t v = 1; v <= n; v++) {
            arr[v - 1] = v * 3;
        }
        for (int64_t i = n - 1; i >= 1; i--) {
            int64_t j = draw(&seed, i + 1);
            int64_t t = arr[i];
            arr[i] = arr[j];
            arr[j] = t;
        }
        arrs[p] = arr;
        ks[p] = draw(&seed, 200000) + 1;
    }
    int64_t check = 0;
    for (int pass = 0; pass < 20; pass++) {
        for (int p = 0; p < 100; p++) {
            check = mix(check, get_winner(arrs[p], n, ks[p]));
        }
    }
    for (int p = 0; p < 100; p++) {
        free(arrs[p]);
    }
    printf("20 passes over 100 arrays of 100000 values: checksum %lld\n", (long long)check);
    return 0;
}
