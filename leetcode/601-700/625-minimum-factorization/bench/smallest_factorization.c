// LeetCode #625: Minimum Factorization -- C mirror of the Kāra bench.
//
// The ★ arm's greedy from the largest digit over the same numbers and
// rounds.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t smallest_factorization(int64_t num) {
    if (num < 10) return num;
    int64_t rest = num, answer = 0, place = 1;
    for (int64_t d = 9; d >= 2; d--) {
        while (rest % d == 0) {
            rest /= d;
            answer += d * place;
            place *= 10;
            if (answer > 2147483647) return 0;
        }
    }
    return rest == 1 ? answer : 0;
}

static int64_t seed = 625;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t *random_numbers(int64_t count) {
    int64_t *numbers = malloc(count * sizeof(int64_t));
    for (int64_t i = 0; i < count; i++) {
        if (i % 2 == 0) {
            int64_t product = 1;
            int64_t n = 1 + next_random() % 10;
            for (int64_t j = 0; j < n; j++) {
                int64_t d = 2 + next_random() % 8;
                if (product * d <= 2147483647) product *= d;
            }
            numbers[i] = product;
        } else {
            int64_t high = next_random();
            int64_t low = next_random();
            numbers[i] = 1 + (high * 65536 + low) % 2147483647;
        }
    }
    return numbers;
}

int main(void) {
    enum { COUNT = 200000, ROUNDS = 50 };
    int64_t *numbers = random_numbers(COUNT);
    int64_t found = 0, checksum = 0;
    for (int r = 0; r < ROUNDS; r++) {
        for (int64_t i = 0; i < COUNT; i++) {
            int64_t a = smallest_factorization(numbers[i]);
            if (a != 0) found++;
            checksum = (checksum * 31 + a) % 1000000007;
        }
    }
    printf("%d numbers, %d rounds: %lld answers, checksum %lld\n", COUNT, ROUNDS, (long long)found, (long long)checksum);
    free(numbers);
    return 0;
}
