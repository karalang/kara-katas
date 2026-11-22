// LeetCode #2739: Total Distance Traveled -- the bench (distance.kara in
// C): (m - 1) / 4 transfers, as many as the additional tank holds.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t distance_traveled(int64_t main_tank, int64_t additional_tank) {
    int64_t transfers = (main_tank - 1) / 4;
    if (additional_tank < transfers) transfers = additional_tank;
    return (main_tank + transfers) * 10;
}

static int64_t seed = 2739;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t count = 1000000, rounds = 100;
    int64_t *mains = malloc(sizeof(int64_t) * count);
    int64_t *extras = malloc(sizeof(int64_t) * count);
    for (int64_t i = 0; i < count; i++) {
        mains[i] = next_random() % 100 + 1;
        extras[i] = next_random() % 100 + 1;
    }
    int64_t sum = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t i = 0; i < count; i++) {
            int64_t d = distance_traveled(mains[i], extras[i]);
            sum += d;
            check = (check * 31 + d + r) % 1000000007;
        }
    }
    printf("%lld pairs of tanks, %lld rounds: distances sum to %lld, checksum %lld\n",
           (long long)count, (long long)rounds, (long long)sum, (long long)check);
    free(mains);
    free(extras);
    return 0;
}
