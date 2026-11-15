// LeetCode #2172: Maximum AND Sum of Array -- the benchmark's C mirror of
// and_sum.kara, over a pointer and a length.

#include <stdio.h>
#include <stdlib.h>

static long long maximum_and_sum(const long long *nums, long long n, long long num_slots) {
    long long powers[16];
    long long p = 1;
    for (long long k = 0; k < num_slots; k++) {
        powers[k] = p;
        p *= 3;
    }
    long long *best = malloc(p * sizeof(long long));
    for (long long i = 0; i < p; i++) best[i] = -1;
    best[0] = 0;
    long long answer = 0;
    for (long long fill = 0; fill < p; fill++) {
        if (best[fill] < 0) continue;
        long long placed = 0, rest = fill;
        while (rest > 0) {
            placed += rest % 3;
            rest /= 3;
        }
        if (placed == n) {
            if (best[fill] > answer) answer = best[fill];
            continue;
        }
        for (long long slot = 0; slot < num_slots; slot++) {
            if (fill / powers[slot] % 3 < 2) {
                long long next = fill + powers[slot];
                long long sum = best[fill] + (nums[placed] & (slot + 1));
                if (sum > best[next]) best[next] = sum;
            }
        }
    }
    free(best);
    return answer;
}

static long long seed = 2172;

static long long next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    long long *row = malloc(100000 * sizeof(long long));
    for (int i = 0; i < 100000; i++) row[i] = next_random() % 15 + 1;
    long long check = 0;
    for (int r = 0; r < 200; r++) {
        long long start = next_random() % 99983;
        long long best = maximum_and_sum(row + start, 18, 9);
        check = (check * 31 + best) % 1000000007;
    }
    printf("200 solves: checksum %lld\n", check);
    free(row);
    return 0;
}
