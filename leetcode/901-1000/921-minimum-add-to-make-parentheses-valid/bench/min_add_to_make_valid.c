// LeetCode #921: Minimum Add to Make Parentheses Valid -- bench: one count
// of the open parentheses. Mirrors min_add_to_make_valid.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t min_add_to_make_valid(const char *s, int64_t len) {
    int64_t open = 0, added = 0;
    for (int64_t i = 0; i < len; i++) {
        if (s[i] == '(') open++;
        else if (open > 0) open--;
        else added++;
    }
    return added + open;
}

static int64_t seed = 921;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    const int64_t rounds = 100, count = 1000, n = 1000;
    // count strings of n parentheses, built once, leaning from ')' to '('
    char **strings = malloc(count * sizeof(char *));
    for (int64_t i = 0; i < count; i++) {
        int64_t lean = 30 + i % 41;
        strings[i] = malloc(n);
        for (int64_t j = 0; j < n; j++) strings[i][j] = next_random() % 100 < lean ? '(' : ')';
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        // each round visits every string, starting from a different one
        for (int64_t i = 0; i < count; i++) {
            int64_t a = min_add_to_make_valid(strings[(r + i) % count], n);
            total += a;
            check = (check * 1000003 + a) % 1000000007;
        }
    }
    printf("%lld rounds over %lld strings of %lld: answers summing to %lld, checksum %lld\n",
           (long long)rounds, (long long)count, (long long)n, (long long)total, (long long)check);
    for (int64_t i = 0; i < count; i++) free(strings[i]);
    free(strings);
    return 0;
}
