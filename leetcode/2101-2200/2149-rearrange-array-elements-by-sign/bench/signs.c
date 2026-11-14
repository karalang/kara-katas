// LeetCode #2149: Rearrange Array Elements by Sign -- the benchmark's C
// mirror of signs.kara.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define N 200000

static int64_t *rearrange_array(const int64_t *nums, int64_t n) {
    int64_t *out = calloc((size_t)n, sizeof(int64_t));
    int64_t positive = 0;
    int64_t negative = 1;
    for (int64_t i = 0; i < n; i++) {
        if (nums[i] > 0) {
            out[positive] = nums[i];
            positive += 2;
        } else {
            out[negative] = nums[i];
            negative += 2;
        }
    }
    return out;
}

static int64_t seed = 2149;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

static int64_t wide(void) {
    int64_t hi = next_random();
    return hi * 32768 + next_random();
}

int main(void) {
    int64_t *lists[4];
    for (int l = 0; l < 4; l++) {
        int64_t *nums = malloc(sizeof(int64_t) * N);
        for (int64_t i = 0; i < N; i++) {
            int64_t size = next_random() % 100000 + 1;
            nums[i] = i < N / 2 ? size : -size;
        }
        for (int64_t i = N - 1; i > 0; i--) {
            int64_t j = wide() % (i + 1);
            int64_t t = nums[i];
            nums[i] = nums[j];
            nums[j] = t;
        }
        lists[l] = nums;
    }
    int64_t check = 0;
    for (int64_t round = 0; round < 25; round++) {
        for (int l = 0; l < 4; l++) {
            int64_t a = wide() % N;
            int64_t b = wide() % N;
            int64_t t = lists[l][a];
            lists[l][a] = lists[l][b];
            lists[l][b] = t;
            int64_t *out = rearrange_array(lists[l], N);
            int64_t at = wide() % N;
            check = (check * 31 + out[0] + out[N - 1] + out[at] + 300000 + round) % 1000000007;
            free(out);
        }
    }
    printf("100 answers: checksum %lld\n", (long long)check);
    for (int l = 0; l < 4; l++) {
        free(lists[l]);
    }
    return 0;
}
