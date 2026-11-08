// LeetCode #1067: Digit Count in Range -- the benchmark's C mirror of
// digit_count.kara: the same place by place count over a million queries.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t count_to(int64_t d, int64_t n) {
    int64_t total = 0;
    int64_t p = 1;
    while (p <= n) {
        int64_t above = n / (p * 10);
        int64_t digit = n / p % 10;
        int64_t below = n % p;
        if (d == 0) {
            if (above == 0) {
                break;
            }
            total += (above - 1) * p;
        } else {
            total += above * p;
        }
        if (digit > d) {
            total += p;
        } else if (digit == d) {
            total += below + 1;
        }
        p *= 10;
    }
    return total;
}

static int64_t digits_count(int64_t d, int64_t low, int64_t high) {
    return count_to(d, high) - count_to(d, low - 1);
}

static int64_t next_random(int64_t *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

#define N 1000000

int main(void) {
    int64_t seed = 1067;
    int64_t (*queries)[3] = malloc(sizeof(int64_t[3]) * N);
    for (int i = 0; i < N; i++) {
        int64_t d = next_random(&seed) % 10;
        int64_t a = (next_random(&seed) * 32768 + next_random(&seed)) % 200000000 + 1;
        int64_t b = (next_random(&seed) * 32768 + next_random(&seed)) % 200000000 + 1;
        queries[i][0] = d;
        queries[i][1] = a < b ? a : b;
        queries[i][2] = a < b ? b : a;
    }
    int64_t calls = 0, total = 0, check = 0;
    for (int i = 0; i < N; i++) {
        int64_t answer = digits_count(queries[i][0], queries[i][1], queries[i][2]);
        total += answer;
        check = (check * 31 + answer) % 1000000007;
        calls += 1;
    }
    printf("%lld calls: answers sum %lld, checksum %lld\n", (long long)calls, (long long)total, (long long)check);
    free(queries);
    return 0;
}
