// LeetCode #914: X of a Kind in a Deck of Cards -- bench: C mirror of the
// counts' greatest common divisor in has_groups_size_x.kara.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t gcd(int64_t a, int64_t b) {
    if (b == 0)
        return a;
    return gcd(b, a % b);
}

static bool has_groups_size_x(const int64_t *deck, int64_t n) {
    int64_t largest = 0;
    for (int64_t i = 0; i < n; i++) {
        if (deck[i] > largest)
            largest = deck[i];
    }
    int64_t *count = calloc(largest + 1, sizeof(int64_t));
    for (int64_t i = 0; i < n; i++)
        count[deck[i]] += 1;
    int64_t g = 0;
    for (int64_t v = 0; v <= largest; v++)
        g = gcd(g, count[v]);
    free(count);
    return g >= 2;
}

static int64_t seed = 914;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t rounds = 20000;
    int64_t n = 1666 * 6;
    int64_t *deck = malloc(sizeof(int64_t) * n);
    for (int64_t v = 0; v < 1666; v++) {
        for (int64_t k = 0; k < 6; k++)
            deck[v * 6 + k] = v * 6;
    }
    int64_t yes = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t high = next_random();
        int64_t i = (high * 32768 + next_random()) % n;
        int64_t old = deck[i];
        deck[i] = old + next_random() % 3 * 6;
        if (deck[i] > 9995)
            deck[i] = old;
        if (has_groups_size_x(deck, n)) {
            yes += 1;
            check = (check * 31 + r) % 1000000007;
        }
        deck[i] = old;
    }
    printf("%lld rounds over %lld cards: %lld partitioned, checksum %lld\n", (long long)rounds, (long long)n,
           (long long)yes, (long long)check);
    free(deck);
    return 0;
}
