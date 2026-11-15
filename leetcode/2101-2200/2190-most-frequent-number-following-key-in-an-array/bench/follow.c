// LeetCode #2190: Most Frequent Number Following Key In an Array -- the
// benchmark's C mirror of follow.kara, over a pointer and a length:
// counts in a list, the leader kept as met.

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static long long most_frequent(const long long *nums, long long n, long long key) {
    long long counts[1001];
    memset(counts, 0, sizeof counts);
    long long best = 0, target = -1;
    for (long long i = 1; i < n; i++) {
        if (nums[i - 1] == key) {
            long long x = nums[i];
            counts[x]++;
            if (counts[x] > best) {
                best = counts[x];
                target = x;
            }
        }
    }
    return target;
}

static long long seed = 2190;

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
    long long *row = malloc(sizeof(long long) * 1000000);
    for (int i = 0; i < 1000000; i++) row[i] = next_random() % 100 + 1;
    long long check = 0;
    for (int r = 0; r < 200000; r++) {
        long long start = big_random() % 999001;
        long long key = row[start];
        check = (check * 31 + most_frequent(row + start, 1000, key)) % 1000000007;
    }
    printf("200000 solves: checksum %lld\n", check);
    free(row);
    return 0;
}
