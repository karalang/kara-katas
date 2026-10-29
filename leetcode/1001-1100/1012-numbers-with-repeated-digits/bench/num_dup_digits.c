// LeetCode #1012 bench: the ★ arm (counting arrangements) over 100,000
// values of n up to a billion, drawn once; each of 40 rounds counts every
// value shifted by its own amount and folds each count into a checksum.

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t arrangements(int64_t free, int64_t slots) {
    int64_t ways = 1;
    for (int64_t j = 0; j < slots; j++) {
        ways *= free - j;
    }
    return ways;
}

static int64_t distinct_up_to(int64_t n) {
    int64_t digits[20];
    int64_t len = 0;
    int64_t rest = n;
    while (rest > 0) {
        digits[len++] = rest % 10;
        rest /= 10;
    }
    for (int64_t i = 0; i < len / 2; i++) {
        int64_t t = digits[i];
        digits[i] = digits[len - 1 - i];
        digits[len - 1 - i] = t;
    }
    int64_t count = 0;
    for (int64_t k = 1; k < len; k++) {
        count += 9 * arrangements(9, k - 1);
    }
    bool seen[10] = {false};
    for (int64_t i = 0; i < len; i++) {
        int64_t d = digits[i];
        int64_t lowest = i == 0 ? 1 : 0;
        for (int64_t smaller = lowest; smaller < d; smaller++) {
            if (!seen[smaller]) {
                count += arrangements(9 - i, len - i - 1);
            }
        }
        if (seen[d]) {
            return count;
        }
        seen[d] = true;
    }
    return count + 1;
}

static int64_t num_dup_digits_at_most_n(int64_t n) {
    return n - distinct_up_to(n);
}

static int64_t seed = 1012;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    int64_t count = 100000;
    int64_t rounds = 40;
    int64_t *values = malloc(sizeof(int64_t) * count);
    for (int64_t i = 0; i < count; i++) {
        int64_t hi = next_random();
        int64_t lo = next_random();
        values[i] = (hi * 32768 + lo) % 1000000000;
    }
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        for (int64_t k = 0; k < count; k++) {
            int64_t n = (values[k] + r * 7919) % 1000000000 + 1;
            check = (check * 31 + num_dup_digits_at_most_n(n)) % 1000000007;
        }
    }
    printf("%lld rounds over %lld values of n: checksum %lld\n", (long long)rounds, (long long)count, (long long)check);
    free(values);
    return 0;
}
