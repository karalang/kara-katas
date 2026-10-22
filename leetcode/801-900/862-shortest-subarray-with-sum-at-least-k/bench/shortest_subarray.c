// LeetCode #862: Shortest Subarray with Sum at Least K -- C mirror of the
// bench program (the ★ arm, prefix sums and a deque of candidate starts;
// the deque is an array with a head and a tail, since every index enters
// it once).
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int64_t shortest_subarray(const int64_t *nums, int64_t n, int64_t k, int64_t *p, int64_t *starts) {
    p[0] = 0;
    for (int64_t i = 0; i < n; i++) {
        p[i + 1] = p[i] + nums[i];
    }
    int64_t best = n + 1;
    int64_t head = 0, tail = 0;
    for (int64_t j = 0; j < n + 1; j++) {
        while (head < tail && p[j] - p[starts[head]] >= k) {
            if (j - starts[head] < best) {
                best = j - starts[head];
            }
            head++;
        }
        while (head < tail && p[starts[tail - 1]] >= p[j]) {
            tail--;
        }
        starts[tail++] = j;
    }
    return best <= n ? best : -1;
}

static int64_t seed = 862;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648;
    return seed / 65536;
}

static int64_t random_value(void) {
    int64_t hi = next_random();
    int64_t lo = next_random();
    return (hi * 32768 + lo) % 200001 - 100000;
}

int main(void) {
    int64_t n = 100000;
    int64_t k = 5000000;
    int64_t rounds = 300;
    int64_t *nums = malloc(n * sizeof(int64_t));
    int64_t *p = malloc((n + 1) * sizeof(int64_t));
    int64_t *starts = malloc((n + 1) * sizeof(int64_t));
    for (int64_t i = 0; i < n; i++) {
        nums[i] = random_value();
    }
    int64_t total = 0;
    int64_t check = 0;
    for (int64_t r = 0; r < rounds; r++) {
        int64_t hi = next_random();
        int64_t lo = next_random();
        int64_t i = (hi * 32768 + lo) % n;
        int64_t old = nums[i];
        nums[i] = random_value();
        int64_t got = shortest_subarray(nums, n, k, p, starts);
        nums[i] = old;
        total += got;
        check = (check * 31 + got + 2) % 1000000007;
    }
    printf("%lld rounds on %lld values, k = %lld: lengths sum to %lld, checksum %lld\n", (long long)rounds,
           (long long)n, (long long)k, (long long)total, (long long)check);
    free(nums);
    free(p);
    free(starts);
    return 0;
}
