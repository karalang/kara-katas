// LeetCode #1224 bench, C mirror of the Kāra ★ arm: each number's count and
// how many numbers have each count, over 10 random arrays of 10^5 numbers
// drawn once, 5 passes; checksum of the answers.
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

static int64_t seed = 1224;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t max_equal_freq(const int64_t *nums, int64_t n) {
    int64_t top = nums[0];
    for (int64_t k = 1; k < n; k++) {
        if (nums[k] > top) {
            top = nums[k];
        }
    }
    int64_t *count = calloc(top + 1, sizeof(int64_t));
    int64_t *with_count = calloc(n + 1, sizeof(int64_t));
    int64_t most = 0, best = 0;
    for (int64_t k = 0; k < n; k++) {
        int64_t x = nums[k];
        with_count[count[x]] -= 1;
        count[x] += 1;
        with_count[count[x]] += 1;
        if (count[x] > most) {
            most = count[x];
        }
        int64_t len = k + 1;
        if (most == 1 || with_count[most] * most + 1 == len || (with_count[most - 1] + 1) * (most - 1) + 1 == len) {
            best = len;
        }
    }
    free(count);
    free(with_count);
    return best;
}

int main(void) {
    static int64_t arrays[10][100000];
    for (int a = 0; a < 10; a++) {
        int64_t values = (int64_t)2 << a;
        for (int k = 0; k < 100000; k++) {
            arrays[a][k] = next_random() % values + 1;
        }
    }
    int64_t total = 0, check = 0;
    for (int pass = 0; pass < 5; pass++) {
        for (int a = 0; a < 10; a++) {
            int64_t answer = max_equal_freq(arrays[a], 100000);
            total += answer;
            check = (check * 131 + answer) % 1000000007;
        }
    }
    printf("10 arrays of 10^5 numbers, 5 passes: lengths total %lld, checksum %lld\n", (long long)total, (long long)check);
    return 0;
}
