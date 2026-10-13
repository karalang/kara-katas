// Benchmark for #494: C mirror of the ★ arm (counting ways by running
// sum); see target_sum.kara. Each number fills a fresh array of counts,
// as the ★ arm does with a fresh `Vec`.
#include <stdio.h>
#include <stdlib.h>

#define ARRAYS 40000
#define N 20

static long long find_target_sum_ways(const long long *nums, long long n, long long target) {
    long long total = 0;
    for (long long i = 0; i < n; i++) {
        total += nums[i];
    }
    if (target > total || target < -total) {
        return 0;
    }
    long long width = 2 * total + 1;
    long long *ways = calloc(width, sizeof(long long));
    ways[total] = 1;
    for (long long i = 0; i < n; i++) {
        long long x = nums[i];
        long long *next = calloc(width, sizeof(long long));
        for (long long s = 0; s < width; s++) {
            if (ways[s] > 0) {
                next[s + x] += ways[s];
                next[s - x] += ways[s];
            }
        }
        free(ways);
        ways = next;
    }
    long long answer = ways[target + total];
    free(ways);
    return answer;
}

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

int main(void) {
    // 40,000 arrays of 20 numbers from 0 to 50 (the problem's most numbers
    // and at most its largest sum), each with a target from -100 to 100,
    // built once, then each solved once.
    static long long arrays[ARRAYS][N], targets[ARRAYS];
    long long seed = 494;
    for (int k = 0; k < ARRAYS; k++) {
        for (int i = 0; i < N; i++) {
            arrays[k][i] = next_random(&seed) % 51;
        }
        targets[k] = next_random(&seed) % 201 - 100;
    }
    long long reachable = 0, checksum = 0;
    for (int k = 0; k < ARRAYS; k++) {
        long long ways = find_target_sum_ways(arrays[k], N, targets[k]);
        if (ways > 0) {
            reachable++;
        }
        checksum = (checksum * 31 + ways) % 1000000007;
    }
    printf("40000 arrays of 20: %lld reachable, checksum %lld\n", reachable, checksum);
    return 0;
}
