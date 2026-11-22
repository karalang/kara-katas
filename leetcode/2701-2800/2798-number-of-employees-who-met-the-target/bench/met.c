// LeetCode #2798: Number of Employees Who Met the Target -- the bench in
// C: the ★ arm over 20000 teams of 50 with hours and targets up to 10^5,
// all drawn first, then each answered 500 times.
#include <stdint.h>
#include <stdio.h>

#define COUNT 20000
#define N 50

static int64_t seed = 2798;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static int64_t number_of_employees_who_met_target(const int64_t *hours, int64_t n, int64_t target) {
    int64_t met = 0;
    for (int64_t i = 0; i < n; i++) met += hours[i] >= target;
    return met;
}

static int64_t hours_[COUNT][N], targets[COUNT];

int main(void) {
    int rounds = 500;
    for (int c = 0; c < COUNT; c++) {
        for (int i = 0; i < N; i++) hours_[c][i] = wide() % 100001;
        targets[c] = wide() % 100001;
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int c = 0; c < COUNT; c++) {
            int64_t a = number_of_employees_who_met_target(hours_[c], N, targets[c]);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    printf("%d teams of 50, %d rounds: met sum to %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
