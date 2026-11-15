// LeetCode #2167: Minimum Time to Remove All Cars Containing Illegal Goods
// -- the benchmark's C mirror of removal.kara: a window of the train as a
// pointer and a length.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t minimum_time(const char *s, int64_t n) {
    int64_t left = 0, best = n;
    for (int64_t i = 0; i < n; i++) {
        if (s[i] == '1') {
            left = left + 2 < i + 1 ? left + 2 : i + 1;
        }
        int64_t t = left + n - 1 - i;
        if (t < best) best = t;
    }
    return best;
}

static int64_t seed = 2167;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    char *train = malloc(400000);
    for (int i = 0; i < 400000; i++) train[i] = next_random() % 3 == 0 ? '1' : '0';
    int64_t check = 0;
    for (int r = 0; r < 100; r++) {
        int64_t hi = next_random();
        int64_t start = (hi * 32768 + next_random()) % 200001;
        int64_t t = minimum_time(train + start, 200000);
        check = (check * 31 + t) % 1000000007;
    }
    printf("100 solves: checksum %lld\n", (long long)check);
    free(train);
    return 0;
}
