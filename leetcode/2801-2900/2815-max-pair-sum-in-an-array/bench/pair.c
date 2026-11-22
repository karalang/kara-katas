// LeetCode #2815: Max Pair Sum in an Array -- the bench in C: the ★ arm
// over 20000 arrays of 100 numbers up to 10^4, all drawn first, then each
// answered 10 times.
#include <stdint.h>
#include <stdio.h>

#define COUNT 20000
#define N 100

static int64_t seed = 2815;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t largest_digit(int64_t x) {
    int64_t top = 0;
    while (x > 0) {
        if (x % 10 > top) top = x % 10;
        x /= 10;
    }
    return top;
}

static int64_t max_sum(const int64_t *nums, int n) {
    int64_t best[10] = {0};
    int64_t answer = -1;
    for (int i = 0; i < n; i++) {
        int64_t x = nums[i], d = largest_digit(x);
        if (best[d] > 0 && best[d] + x > answer) answer = best[d] + x;
        if (x > best[d]) best[d] = x;
    }
    return answer;
}

static int64_t arrays[COUNT][N];

int main(void) {
    int rounds = 10;
    for (int a = 0; a < COUNT; a++)
        for (int i = 0; i < N; i++) arrays[a][i] = next_random() % 10000 + 1;
    int64_t total = 0, check = 0;
    for (int64_t r = 0; r < rounds; r++)
        for (int a = 0; a < COUNT; a++) {
            int64_t v = max_sum(arrays[a], N);
            total += v;
            check = (check * 31 + v + 2 + r) % 1000000007;
        }
    printf("%d arrays of 100, %d rounds: sums total %lld, checksum %lld\n", COUNT, rounds, (long long)total, (long long)check);
    return 0;
}
