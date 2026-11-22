// LeetCode #2897: Apply Operations on Array to Maximize Sum of Squares --
// the bench's C mirror (squares.kara).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t seed = 2897;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t a = next_random();
    return a * 32768 + next_random();
}

static int64_t max_sum(const int64_t *nums, int64_t n, int64_t k) {
    const int64_t modulus = 1000000007;
    int64_t holders[31] = {0};
    for (int64_t i = 0; i < n; i++)
        for (int b = 0; b < 31; b++)
            if ((nums[i] >> b) & 1) holders[b]++;
    int64_t sum = 0;
    for (int64_t t = 0; t < k; t++) {
        int64_t value = 0;
        for (int b = 0; b < 31; b++)
            if (holders[b] > 0) {
                holders[b]--;
                value |= (int64_t)1 << b;
            }
        sum = (sum + value * value) % modulus;
    }
    return sum;
}

int main(void) {
    enum { COUNT = 20, ROUNDS = 20, N = 10000 };
    int64_t *nums[COUNT];
    int64_t ks[COUNT];
    for (int c = 0; c < COUNT; c++) {
        nums[c] = malloc(sizeof(int64_t) * N);
        for (int i = 0; i < N; i++) {
            if (c % 2 == 0) {
                nums[c][i] = wide() % 1000000000 + 1;
            } else {
                int64_t a = next_random() % 30;
                int64_t b = next_random() % 30;
                nums[c][i] = ((int64_t)1 << a) | ((int64_t)1 << b);
            }
        }
        ks[c] = wide() % N + 1;
    }
    int64_t total = 0, check = 0;
    for (int r = 0; r < ROUNDS; r++)
        for (int c = 0; c < COUNT; c++) {
            int64_t s = max_sum(nums[c], N, ks[c]);
            total += s;
            check = (check * 31 + s + r) % 1000000007;
        }
    printf("%d arrays of %d, %d rounds: sums total %lld, checksum %lld\n", COUNT, N, ROUNDS,
           (long long)total, (long long)check);
    for (int c = 0; c < COUNT; c++) free(nums[c]);
    return 0;
}
