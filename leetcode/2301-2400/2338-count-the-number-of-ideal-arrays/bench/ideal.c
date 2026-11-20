// LeetCode #2338: Count the Number of Ideal Arrays -- the bench, the ★ arm
// in C: the strictly increasing divisor chains of each length counted
// level by level, each length k + 1 spread over the n places in
// C(n - 1, k) ways.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define MODULUS 1000000007LL
#define LONGEST 14

static int64_t power(int64_t base, int64_t exp) {
    int64_t result = 1;
    base %= MODULUS;
    while (exp > 0) {
        if (exp % 2 == 1) result = result * base % MODULUS;
        base = base * base % MODULUS;
        exp /= 2;
    }
    return result;
}

static int64_t ideal_arrays(int64_t n, int64_t max_value) {
    int64_t ways[LONGEST];
    ways[0] = 1;
    for (int64_t k = 1; k < LONGEST; k++)
        ways[k] = ways[k - 1] * ((n - 1 - k + 1) % MODULUS) % MODULUS * power(k, MODULUS - 2) % MODULUS;
    int64_t size = max_value + 1;
    int64_t *ends = malloc(size * sizeof(int64_t));
    for (int64_t v = 0; v < size; v++) ends[v] = 1;
    ends[0] = 0;
    int64_t answer = 0;
    for (int k = 0; k < LONGEST; k++) {
        int64_t total = 0;
        for (int64_t v = 1; v < size; v++) total = (total + ends[v]) % MODULUS;
        answer = (answer + total * ways[k]) % MODULUS;
        int64_t *following = calloc(size, sizeof(int64_t));
        for (int64_t d = 1; d < size; d++) {
            if (ends[d] != 0) {
                for (int64_t m = 2 * d; m < size; m += d)
                    following[m] = (following[m] + ends[d]) % MODULUS;
            }
        }
        free(ends);
        ends = following;
    }
    free(ends);
    return answer;
}

static int64_t scrambled(int64_t index) { return index * 2654435761LL % 2147483647LL; }

int main(void) {
    int64_t check = 0;
    for (int64_t q = 0; q < 300; q++) {
        int64_t n = 2 + scrambled(q + 1) % 9999;
        int64_t max_value = 5000 + scrambled(q + 1001) % 5001;
        check = (check * 31 + ideal_arrays(n, max_value)) % 1000000007;
    }
    printf("300 queries of n up to 10^4 and maxValue 5000 to 10^4: checksum %lld\n", (long long)check);
    return 0;
}
