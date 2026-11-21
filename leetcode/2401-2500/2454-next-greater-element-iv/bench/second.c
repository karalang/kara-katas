// LeetCode #2454: Next Greater Element IV -- bench, C mirror of
// second.kara: two monotonic stacks, the first waiting for one greater
// value and the second for another.

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static void second_greater_element(const int64_t *nums, int64_t n, int64_t *answer, int64_t *first, int64_t *second) {
    int64_t f = 0, s = 0;
    for (int64_t j = 0; j < n; j++) {
        answer[j] = -1;
    }
    for (int64_t j = 0; j < n; j++) {
        while (s > 0 && nums[second[s - 1]] < nums[j]) {
            answer[second[--s]] = nums[j];
        }
        int64_t cut = f;
        while (cut > 0 && nums[first[cut - 1]] < nums[j]) {
            cut -= 1;
        }
        for (int64_t i = cut; i < f; i++) {
            second[s++] = first[i];
        }
        f = cut;
        first[f++] = j;
    }
}

static int64_t seed = 2454;

static int64_t next_random(void) {
    seed = (seed * 1103515245 + 12345) % 2147483648LL;
    return seed / 65536;
}

int main(void) {
    const int64_t n = 100000;
    int64_t *arrays[10];
    for (int a = 0; a < 10; a++) {
        arrays[a] = malloc(sizeof(int64_t) * n);
        for (int64_t i = 0; i < n; i++) {
            int64_t hi = next_random();
            arrays[a][i] = (hi * 32768 + next_random()) % 1000000001;
        }
    }
    int64_t *answer = malloc(sizeof(int64_t) * n);
    int64_t *first = malloc(sizeof(int64_t) * n);
    int64_t *second = malloc(sizeof(int64_t) * n);
    int64_t check = 0;
    for (int64_t p = 0; p < 20; p++) {
        for (int64_t a = 0; a < 10; a++) {
            arrays[a][(p * 7919 + a) % n] = check % 1000000001;
            second_greater_element(arrays[a], n, answer, first, second);
            for (int64_t i = 0; i < n; i++) {
                check = (check * 31 + answer[i] + 1) % 1000000007;
            }
            check = (check + p) % 1000000007;
        }
    }
    printf("20 passes over 10 arrays of 10^5 values: checksum %lld\n", (long long)check);
    for (int a = 0; a < 10; a++) free(arrays[a]);
    free(answer);
    free(first);
    free(second);
    return 0;
}
