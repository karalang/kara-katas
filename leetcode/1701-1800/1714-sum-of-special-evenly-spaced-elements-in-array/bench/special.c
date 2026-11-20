// LeetCode #1714: Sum Of Special Evenly-Spaced Elements In Array -- the C
// mirror of the bench (special.kara): the queries taken in order of their
// step, a small step's sums built from the back and a large step's walked,
// on 5 random problems of 50000 values and 150000 queries, each answered 4
// times.
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static const int *step_of;

// by step, then by index, as a stable sort by step leaves them
static int by_step(const void *a, const void *b) {
    long i = *(const long *)a;
    long j = *(const long *)b;
    int x = step_of[2 * i + 1];
    int y = step_of[2 * j + 1];
    if (x != y) {
        return (x > y) - (x < y);
    }
    return (i > j) - (i < j);
}

// the floor of the square root, an f64 estimate stepped to the root
static long isqrt(long n) {
    long r = (long)sqrt((double)n);
    while (r * r > n) {
        r--;
    }
    while ((r + 1) * (r + 1) <= n) {
        r++;
    }
    return r;
}

// queries[2 i] is the start, queries[2 i + 1] the step
static int *solve(const int *nums, long n, const int *queries, long q) {
    const long long modulus = 1000000007;
    long small = isqrt(n);
    int *answer = calloc(q, sizeof(int));
    long *order = malloc(sizeof(long) * q);
    for (long i = 0; i < q; i++) {
        order[i] = i;
    }
    step_of = queries;
    qsort(order, q, sizeof(long), by_step);
    long long *sums = calloc(n, sizeof(long long));
    long built = 0;
    for (long k = 0; k < q; k++) {
        long i = order[k];
        long x = queries[2 * i];
        long y = queries[2 * i + 1];
        if (y <= small) {
            if (y != built) {
                for (long j = n - 1; j >= 0; j--) {
                    long long after = j + y < n ? sums[j + y] : 0;
                    sums[j] = (nums[j] + after) % modulus;
                }
                built = y;
            }
            answer[i] = (int)sums[x];
        } else {
            long long total = 0;
            for (long j = x; j < n; j += y) {
                total += nums[j];
            }
            answer[i] = (int)(total % modulus);
        }
    }
    free(sums);
    free(order);
    return answer;
}

static long long next_random(long long *seed) {
    *seed = (*seed * 1103515245 + 12345) % 2147483648LL;
    return *seed / 65536;
}

static long long wide(long long *seed) {
    long long a = next_random(seed);
    return a * 32768 + next_random(seed);
}

int main(void) {
    const int count = 5;
    const long long rounds = 4;
    const long n = 50000;
    const long q = 150000;
    long long seed = 1714;
    int *nums = malloc(sizeof(int) * count * n);
    int *queries = malloc(sizeof(int) * count * q * 2);
    for (int p = 0; p < count; p++) {
        for (long i = 0; i < n; i++) {
            nums[p * n + i] = (int)(wide(&seed) % 1000000000);
        }
        for (long i = 0; i < q; i++) {
            long long x = wide(&seed) % n;
            long long y;
            if (next_random(&seed) % 2 == 0) {
                y = next_random(&seed) % 223 + 1;
            } else {
                y = wide(&seed) % n + 1;
            }
            queries[(p * q + i) * 2] = (int)x;
            queries[(p * q + i) * 2 + 1] = (int)y;
        }
    }
    long long sum = 0;
    long long check = 0;
    for (long long r = 0; r < rounds; r++) {
        for (int p = 0; p < count; p++) {
            int *answer = solve(nums + p * n, n, queries + p * q * 2, q);
            for (long i = 0; i < q; i++) {
                sum += answer[i];
                check = (check * 31 + answer[i] + r) % 1000000007;
            }
            free(answer);
        }
    }
    printf("%d problems of %ld values and %ld queries, %lld rounds: answers sum to %lld, checksum %lld\n", count, n, q, rounds, sum, check);
    free(nums);
    free(queries);
    return 0;
}
