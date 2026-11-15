// LeetCode #2183: Count Array Pairs Divisible by K -- the benchmark's C
// mirror of pairs_divisible.kara, over a pointer and a length.

#include <stdio.h>
#include <stdlib.h>

static long long gcd(long long a, long long b) {
    while (b != 0) {
        long long r = a % b;
        a = b;
        b = r;
    }
    return a;
}

static long long count_pairs(const long long *nums, long long n, long long k) {
    long long *by_gcd = calloc(k + 1, sizeof(long long));
    for (long long i = 0; i < n; i++) by_gcd[gcd(nums[i], k)]++;
    long long divisors[256];
    long long count = 0;
    for (long long d = 1; d * d <= k; d++) {
        if (k % d == 0) {
            if (by_gcd[d] > 0) divisors[count++] = d;
            if (d * d != k && by_gcd[k / d] > 0) divisors[count++] = k / d;
        }
    }
    long long pairs = 0;
    for (long long a = 0; a < count; a++) {
        for (long long b = a; b < count; b++) {
            long long g = divisors[a];
            long long h = divisors[b];
            if (g * h % k == 0) {
                if (a == b)
                    pairs += by_gcd[g] * (by_gcd[g] - 1) / 2;
                else
                    pairs += by_gcd[g] * by_gcd[h];
            }
        }
    }
    free(by_gcd);
    return pairs;
}

static long long seed = 2183;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long big_random(void) {
    long long a = next_random();
    long long b = next_random();
    return a * 32768 + b;
}

int main(void) {
    long long *row = malloc(1000000 * sizeof(long long));
    for (int i = 0; i < 1000000; i++) row[i] = big_random() % 100000 + 1;
    long long check = 0;
    for (int r = 0; r < 200; r++) {
        long long start = big_random() % 900001;
        long long k = big_random() % 100000 + 1;
        long long found = count_pairs(row + start, 100000, k);
        check = (check * 31 + found % 1000000007) % 1000000007;
    }
    printf("200 solves: checksum %lld\n", check);
    free(row);
    return 0;
}
