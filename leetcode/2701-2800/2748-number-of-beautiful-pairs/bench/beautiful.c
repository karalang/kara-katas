// LeetCode #2748: Number of Beautiful Pairs -- the bench (beautiful.kara
// in C): the first digits seen so far counted, each number adding the
// counts of the digits coprime to its last digit.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t gcd(int64_t a, int64_t b) { return b == 0 ? a : gcd(b, a % b); }

static int64_t count_beautiful_pairs(const int64_t *nums, int n) {
    int64_t firsts[10] = {0};
    int64_t pairs = 0;
    for (int i = 0; i < n; i++) {
        int64_t x = nums[i], last = x % 10;
        for (int64_t d = 1; d < 10; d++)
            if (gcd(d, last) == 1) pairs += firsts[d];
        int64_t first = x;
        while (first >= 10) first /= 10;
        firsts[first]++;
    }
    return pairs;
}

static int64_t seed = 2748;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int count = 20000, rounds = 10;
    int64_t *lists = malloc(sizeof(int64_t) * count * 100);
    for (int k = 0; k < count; k++)
        for (int i = 0; i < 100; i++) {
            int64_t x = next_random() % 9999 + 1;
            lists[k * 100 + i] = x % 10 == 0 ? x + 1 : x;
        }
    int64_t sum = 0, check = 0;
    for (int r = 0; r < rounds; r++)
        for (int k = 0; k < count; k++) {
            int64_t pairs = count_beautiful_pairs(lists + k * 100, 100);
            sum += pairs;
            check = (check * 31 + pairs + r) % 1000000007;
        }
    printf("%d lists of 100 numbers, %d rounds: pairs sum to %lld, checksum %lld\n", count, rounds, (long long)sum, (long long)check);
    free(lists);
    return 0;
}
