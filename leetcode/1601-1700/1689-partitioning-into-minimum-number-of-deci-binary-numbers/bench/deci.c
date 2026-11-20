// LeetCode #1689: Partitioning Into Minimum Number Of Deci-Binary Numbers
// -- the bench's C mirror: the ★ arm on 100 random numbers of 100000
// digits, all drawn first, each answered 50 times.

#include <stdint.h>
#include <stdio.h>

#define COUNT 100
#define SIZE 100000
#define ROUNDS 50

static int32_t min_partitions(const char *n, int64_t len) {
    int32_t largest = 0;
    for (int64_t i = 0; i < len; i++) {
        int32_t d = n[i] - '0';
        if (d > largest) largest = d;
    }
    return largest;
}

// ---- the harness ----------------------------------------------------------

static int64_t seed = 1689;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    static char numbers[COUNT][SIZE];
    for (int c = 0; c < COUNT; c++) {
        int64_t top = next_random() % 9 + 1;
        numbers[c][0] = (char)('0' + next_random() % top + 1);
        for (int i = 1; i < SIZE; i++) numbers[c][i] = (char)('0' + next_random() % (top + 1));
    }
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < ROUNDS; r++) {
        for (int c = 0; c < COUNT; c++) {
            int32_t answer = min_partitions(numbers[c], SIZE);
            total += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    printf("%d numbers of %d digits, %d rounds: answers sum to %lld, checksum %lld\n", COUNT, SIZE, ROUNDS, (long long)total, (long long)check);
    return 0;
}
