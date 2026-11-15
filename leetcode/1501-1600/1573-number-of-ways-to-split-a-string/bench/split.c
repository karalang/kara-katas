// LeetCode #1573: Number of Ways to Split a String -- bench: the ★ arm (the
// two gaps between the ones multiplied) over 20 strings of 500000
// characters, each with its own odds of a '1' from 1 in 1 to 1 in 1000,
// built once; then 10 rounds answering all 20, 200 answers.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int64_t num_ways(const char *s, int64_t n) {
    const int64_t m = 1000000007;
    int64_t cap = 16, t = 0;
    int64_t *ones = malloc(sizeof(int64_t) * cap);
    for (int64_t i = 0; i < n; i++) {
        if (s[i] == '1') {
            if (t == cap) {
                cap *= 2;
                ones = realloc(ones, sizeof(int64_t) * cap);
            }
            ones[t++] = i;
        }
    }
    int64_t ways;
    if (t == 0) {
        ways = (n - 1) * (n - 2) / 2 % m;
    } else if (t % 3 != 0) {
        ways = 0;
    } else {
        int64_t k = t / 3;
        ways = (ones[k] - ones[k - 1]) * (ones[2 * k] - ones[2 * k - 1]) % m;
    }
    free(ones);
    return ways;
}

static int64_t seed = 1573;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t mix(int64_t check, int64_t x) { return (check * 31 + x + 1) % 1000000007; }

int main(void) {
    const int64_t n = 500000;
    char *strings[20];
    for (int v = 0; v < 20; v++) {
        int64_t odds = next_random() % 1000 + 1;
        strings[v] = malloc(n + 1);
        for (int64_t i = 0; i < n; i++) {
            strings[v][i] = next_random() % odds == 0 ? '1' : '0';
        }
        strings[v][n] = 0;
    }
    int64_t check = 0, total = 0;
    for (int r = 0; r < 10; r++) {
        for (int v = 0; v < 20; v++) {
            int64_t ways = num_ways(strings[v], n);
            total += ways;
            check = mix(check, ways);
        }
    }
    printf("200 answers over 20 strings of %lld characters: ways total %lld, checksum %lld\n", (long long)n,
           (long long)total, (long long)check);
    for (int v = 0; v < 20; v++) {
        free(strings[v]);
    }
    return 0;
}
