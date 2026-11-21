// LeetCode #2522: Partition String Into Substrings With Values at Most K --
// C mirror of the benchmark (greedy.kara): the same strings, passes, order
// and checksum.
#include <stdint.h>
#include <stdio.h>

#define LEN 100000

static int64_t minimum_partition(const char *s, int64_t n, int64_t k) {
    int64_t parts = 1, value = 0;
    for (int64_t i = 0; i < n; i++) {
        int64_t d = s[i] - '0';
        if (d > k) return -1;
        value = value * 10 + d;
        if (value > k) {
            parts++;
            value = d;
        }
    }
    return parts;
}

static int64_t seed = 2522;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static char strings[20][LEN];

int main(void) {
    for (int t = 0; t < 20; t++)
        for (int i = 0; i < LEN; i++) strings[t][i] = (char)('0' + next_random() % 9 + 1);
    const int passes = 50;
    int64_t check = 0;
    for (int p = 0; p < passes; p++)
        for (int t = 0; t < 20; t++)
            check = (check * 31 + minimum_partition(strings[t], LEN, check % 999999992 + 9) + p) % 1000000007;
    printf("%d passes over 20 strings of 10^5 digits: checksum %lld\n", passes, (long long)check);
    return 0;
}
