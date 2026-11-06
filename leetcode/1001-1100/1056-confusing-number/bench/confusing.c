// LeetCode #1056: Confusing Number -- the benchmark, mirror of confusing.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int confusing_number(int64_t n) {
    static const int64_t turned[10] = {0, 1, -1, -1, -1, -1, 9, -1, 8, 6};
    int64_t rest = n;
    int64_t upside = 0;
    while (rest > 0) {
        int64_t d = turned[rest % 10];
        if (d < 0) {
            return 0;
        }
        upside = upside * 10 + d;
        rest /= 10;
    }
    return upside != n;
}

static int64_t seed = 1056;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t count = 500000;
    const int64_t rounds = 20;
    const int64_t turning[5] = {0, 1, 6, 8, 9};
    const int64_t other[5] = {2, 3, 4, 5, 7};
    int64_t *numbers = malloc(sizeof(int64_t) * count);
    for (int64_t i = 0; i < count; i++) {
        int64_t digits = 6 + next_random() % 5;
        int64_t spoiled = -1;
        if (next_random() % 8 == 0) {
            spoiled = next_random() % digits;
        }
        int64_t n = turning[1 + next_random() % 4];
        for (int64_t k = 1; k < digits; k++) {
            int64_t d = k == spoiled ? other[next_random() % 5] : turning[next_random() % 5];
            n = n * 10 + d;
        }
        numbers[i] = n;
    }
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t found = 0;
        for (int64_t i = 0; i < count; i++) {
            int64_t n = numbers[i];
            if (confusing_number(n)) {
                found += 1;
                check = (check + n % 1000) % 1000000007;
            }
        }
        total += found;
        check = (check * 131 + found) % 1000000007;
    }
    printf("%lld numbers, %lld rounds: %lld confusing, checksum %lld\n", (long long)count,
           (long long)rounds, (long long)total, (long long)check);
    free(numbers);
    return 0;
}
