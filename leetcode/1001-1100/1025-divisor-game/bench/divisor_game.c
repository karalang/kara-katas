// LeetCode #1025: Divisor Game -- bench
// Mirrors ./divisor_game.kara; see ../README.md § Benchmarks.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int64_t *items;
    int len, cap;
} List;

static void push(List *l, int64_t x) {
    if (l->len == l->cap) {
        l->cap = l->cap ? 2 * l->cap : 4;
        l->items = realloc(l->items, sizeof(int64_t) * (size_t)l->cap);
    }
    l->items[l->len++] = x;
}

static bool divisor_game(int64_t n) {
    List *divisors = calloc((size_t)(n + 1), sizeof(List));
    for (int64_t x = 1; x <= n / 2; x++) {
        for (int64_t m = 2 * x; m <= n; m += x) {
            push(&divisors[m], x);
        }
    }
    bool *wins = calloc((size_t)(n + 1), sizeof(bool));
    for (int64_t m = 2; m <= n; m++) {
        for (int k = 0; k < divisors[m].len; k++) {
            if (!wins[m - divisors[m].items[k]]) {
                wins[m] = true;
                break;
            }
        }
    }
    bool answer = wins[n];
    for (int64_t m = 0; m <= n; m++) free(divisors[m].items);
    free(divisors);
    free(wins);
    return answer;
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    return *seed / 65536;
}

int main(void) {
    const int count = 100;
    const int rounds = 100;
    int64_t seed = 1025;
    int64_t games[100];
    for (int i = 0; i < count; i++) games[i] = 500 + next_random(&seed) % 501;
    int64_t wins = 0, check = 0;
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < count; i++) {
            bool alice = divisor_game(games[i]);
            if (alice) wins++;
            check = (check * 131 + games[i] * 2 + (alice ? 1 : 0)) % 1000000007;
        }
    }
    printf("%d games of n from 500 to 1000, %d rounds: Alice wins %lld, checksum %lld\n", count, rounds,
           (long long)wins, (long long)check);
    return 0;
}
