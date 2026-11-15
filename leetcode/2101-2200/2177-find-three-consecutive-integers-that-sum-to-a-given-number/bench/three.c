// LeetCode #2177: Find Three Consecutive Integers That Sum to a Given
// Number -- the benchmark's C mirror of three.kara: each answer a heap
// list of three, or none.

#include <stdio.h>
#include <stdlib.h>

static long long *sum_of_three(long long num, long long *len) {
    if (num % 3 != 0) {
        *len = 0;
        return NULL;
    }
    long long x = num / 3;
    long long *three = malloc(3 * sizeof(long long));
    three[0] = x - 1;
    three[1] = x;
    three[2] = x + 1;
    *len = 3;
    return three;
}

static long long seed = 2177;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    long long *row = malloc(1000000 * sizeof(long long));
    for (int i = 0; i < 1000000; i++) {
        long long a = next_random();
        long long b = next_random();
        long long c = next_random();
        row[i] = ((a * 32768 + b) * 32768 + c) % 1000000000000001LL;
    }
    long long found = 0, check = 0;
    for (int pass = 0; pass < 2; pass++) {
        for (int i = 0; i < 1000000; i++) {
            long long len;
            long long *three = sum_of_three(row[i] + pass, &len);
            if (len == 3) {
                found++;
                check = (check * 31 + three[2] % 1000000007) % 1000000007;
            }
            free(three);
        }
    }
    printf("2000000 solves: %lld found, checksum %lld\n", found, check);
    free(row);
    return 0;
}
