// LeetCode #891 bench: the counting arm (a count of each value) on 400
// arrays of 100,000 numbers from 1 to 100,000. The same algorithm as
// sum_subseq_widths.kara.
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MODULUS 1000000007
#define N 100000

static int64_t sum_subseq_widths(const int64_t *nums, int64_t n) {
    int64_t largest = 0;
    for (int64_t i = 0; i < n; i++) if (nums[i] > largest) largest = nums[i];
    int64_t *count = calloc(largest + 1, sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) count[nums[i]]++;
    int64_t *pow = malloc((n + 1) * sizeof(int64_t));
    pow[0] = 1;
    for (int64_t i = 1; i <= n; i++) pow[i] = pow[i - 1] * 2 % MODULUS;
    int64_t total = 0, p = 0;
    for (int64_t v = 0; v <= largest; v++) {
        int64_t c = count[v];
        if (c > 0) {
            int64_t block = pow[c] - 1;
            int64_t as_max = pow[p] * block % MODULUS;
            int64_t as_min = pow[n - p - c] * block % MODULUS;
            total = (total + v * (as_max - as_min)) % MODULUS;
            p += c;
        }
    }
    free(count);
    free(pow);
    return (total + MODULUS) % MODULUS;
}

static int64_t seed = 891;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

int main(void) {
    int64_t sum = 0, check = 0;
    int64_t *nums = malloc(N * sizeof(int64_t));
    for (int c = 0; c < 400; c++) {
        for (int i = 0; i < N; i++) nums[i] = 1 + next_random() % 100000;
        int64_t got = sum_subseq_widths(nums, N);
        sum = (sum + got) % MODULUS;
        check = (check * 131 + got) % MODULUS;
    }
    free(nums);
    printf("400 arrays of 100000 numbers: widths sum to %lld, checksum %lld\n", (long long)sum, (long long)check);
    return 0;
}
