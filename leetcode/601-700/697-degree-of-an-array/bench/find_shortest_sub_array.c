// LeetCode #697: Degree of an Array -- bench program, C mirror of the table arm.
#include <stdio.h>
#include <stdlib.h>

#define LEN 50000
#define SIZE 50000

static long long seed = 697;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static long long find_shortest_sub_array(const long long *nums, long long n) {
    long long *count = calloc(SIZE, sizeof(long long));
    long long *first = malloc(SIZE * sizeof(long long));
    long long *last = calloc(SIZE, sizeof(long long));
    for (long long x = 0; x < SIZE; x++) first[x] = -1;
    for (long long i = 0; i < n; i++) {
        long long x = nums[i];
        if (first[x] < 0) first[x] = i;
        last[x] = i;
        count[x]++;
    }
    long long degree = 0, best = n;
    for (long long x = 0; x < SIZE; x++) {
        if (count[x] == 0) continue;
        long long span = last[x] - first[x] + 1;
        if (count[x] > degree || (count[x] == degree && span < best)) {
            degree = count[x];
            best = span;
        }
    }
    free(count);
    free(first);
    free(last);
    return best;
}

int main(void) {
    static long long arrays[40][LEN];
    for (int k = 0; k < 40; k++) {
        long long range = 1 + 1250 * k;
        for (int i = 0; i < LEN; i++) {
            long long a = next_random();
            long long b = next_random();
            arrays[k][i] = (a * 65536 + b) % range;
        }
    }
    int rounds = 20;
    long long total = 0, checksum = 0;
    for (int r = 0; r < rounds; r++)
        for (int k = 0; k < 40; k++) {
            long long c = find_shortest_sub_array(arrays[k], LEN);
            total += c;
            checksum = (checksum * 31 + c) % 1000000007;
        }
    printf("%d rounds of 40 arrays of 50000: shortest spans sum to %lld, checksum %lld\n", rounds, total, checksum);
    return 0;
}
