// LeetCode #1744: Can You Eat Your Favorite Candy on Your Favorite Day?
// -- the bench (eat.kara in C): prefix sums, then two comparisons a query.
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

enum { COUNT = 10, ROUNDS = 30, N = 100000 };

static void can_eat(const int32_t *candies, int64_t n, const int32_t (*queries)[3], int64_t q, bool *answers) {
    int64_t *before = malloc(sizeof(int64_t) * (n + 1));
    before[0] = 0;
    for (int64_t i = 0; i < n; i++) before[i + 1] = before[i] + candies[i];
    for (int64_t i = 0; i < q; i++) {
        int64_t t = queries[i][0], day = queries[i][1], cap = queries[i][2];
        answers[i] = day + 1 <= before[t + 1] && (day + 1) * cap > before[t];
    }
    free(before);
}

static int64_t seed = 1744;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

int main(void) {
    static int32_t candies[COUNT][N];
    static int32_t queries[COUNT][N][3];
    for (int c = 0; c < COUNT; c++) {
        int64_t total = 0;
        for (int64_t i = 0; i < N; i++) {
            candies[c][i] = (int32_t)(next_random() % 20 + 1);
            total += candies[c][i];
        }
        for (int64_t i = 0; i < N; i++) {
            int64_t t = wide() % N;
            int64_t day = wide() % total;
            int64_t cap = next_random() % 30 + 1;
            queries[c][i][0] = (int32_t)t;
            queries[c][i][1] = (int32_t)day;
            queries[c][i][2] = (int32_t)cap;
        }
    }
    bool *answers = malloc(sizeof(bool) * N);
    int64_t yes = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            can_eat(candies[c], N, queries[c], N, answers);
            int64_t here = 0;
            for (int64_t i = 0; i < N; i++) {
                if (answers[i]) {
                    here += 1;
                    check = (check + i * 7 + r) % 1000000007;
                }
            }
            yes += here;
        }
    }
    printf("%d problems of %d types and %d queries, %d rounds: %lld yes, checksum %lld\n", COUNT, N, N, ROUNDS, (long long)yes, (long long)check);
    free(answers);
    return 0;
}
